import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai

st.set_page_config(page_title="iruKa Phase 3: Financial Deep Dive", layout="wide", page_icon="🔬")
st.title("🔬 iruKa Phase 3: Soi Báo Cáo Tài Chính Nội Bộ Băng Đảng")

# ==========================================
# 1. LOAD TOÀN BỘ DATABASE (NETWORK + FINANCE)
# ==========================================
@st.cache_data
def load_all_data():
    df_meso = pd.read_csv("db_meso_community.csv")
    df_micro = pd.read_csv("db_micro_nodes.csv")
    df_profiles = pd.read_csv("db_company_profiles.csv")
    
    # [ĐÃ FIX]: Đọc từ file database đã được gom ở bước ETL
    df_fin_year = pd.read_csv("db_finance_year.csv")
    df_ratios = pd.read_csv("db_finance_ratios.csv")
    
    # Từ điển Ngành
    df_sector = pd.read_csv("db_sector_map.csv")
    sector_map = dict(zip(df_sector['Symbol'], df_sector['Sector']))
    
    return df_meso, df_micro, df_profiles, df_fin_year, df_ratios, sector_map

df_meso, df_micro, df_profiles, df_fin_year, df_ratios, SECTOR_MAP = load_all_data()

# Hàm format số tiền cho dễ đọc (Giả định chia 1 tỷ)
def format_currency(val):
    try:
        if pd.isna(val): return "N/A"
        return f"{float(val) / 1e6:,.1f} Tỷ"
    except:
        return "N/A"

def format_ratio(val):
    try:
        if pd.isna(val): return "N/A"
        return f"{float(val):.2f}"
    except:
        return "N/A"

# ==========================================
# 2. CÔNG CỤ ĐIỀU HƯỚNG (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("⚙️ Bảng Điều Khiển")
    years = sorted(df_micro['Year'].unique())
    selected_year = st.selectbox("Chọn Năm Phân Tích:", years, index=len(years)-1)
    
    st.markdown("---")
    api_key = st.text_input("🔑 Nhập Gemini API Key:", type="password")

# ==========================================
# 3. CHUẨN BỊ DỮ LIỆU TỪNG BĂNG ĐẢNG VÀ TẠO TABS
# ==========================================
meso_year = df_meso[df_meso['Year'] == selected_year]
leaders = meso_year['Leader'].tolist()

if not leaders:
    st.warning(f"Không có dữ liệu Băng đảng cho năm {selected_year}.")
    st.stop()

# Dàn các băng đảng thành các Tabs ngang
tabs = st.tabs([f"👑 Nhóm {l}" for l in leaders])

# Lặp qua từng Băng đảng để Render nội dung vào Tab tương ứng
for leader, tab in zip(leaders, tabs):
    with tab:
        group_info = meso_year[meso_year['Leader'] == leader].iloc[0]
        members = group_info['Members'].split(', ')

        # Tìm ngành chi phối
        sectors = [SECTOR_MAP.get(m, 'Khác') for m in members]
        dom_sector = max(set(sectors), key=sectors.count)

        st.markdown(f"### 🛡️ Băng đảng **{leader}** | Ngành chi phối: **{dom_sector}**")
        
        display_data = []
        finance_prompt_context = "" # [ĐÃ FIX]: Khai báo đúng tên biến

        for sym in members:
            sec = SECTOR_MAP.get(sym, 'Khác')
            tag = sec if sec == dom_sector else f"🔥 Ngoại đạo ({sec})"
            power = df_micro[(df_micro['Symbol'] == sym) & (df_micro['Year'] == selected_year)]['Power_Score'].values[0]
            
            # --- TRÍCH XUẤT DỮ LIỆU TÀI CHÍNH TỪ CSV GỐC ---
            fin_y = df_fin_year[(df_fin_year['Symbol'] == sym) & (df_fin_year['Nam'] == selected_year)]
            ratio_y = df_ratios[(df_ratios['Symbol'] == sym) & (df_ratios['Nam'] == selected_year)]
            
            # Lấy Doanh Thu và Lợi Nhuận (Đã tối ưu theo chuẩn file CSV của bạn)
            if not fin_y.empty:
                row_data = fin_y.iloc[0]
                
                # Ưu tiên lấy TotalIncome (Tổng thu nhập chuẩn hóa), dự phòng DTTBHCCDV
                doanh_thu_raw = row_data.get('TotalIncome', 
                                row_data.get('DTTBHCCDV', np.nan))
                
                # Lấy Lợi nhuận ròng
                loi_nhuan_raw = row_data.get('NetIncome', 
                                row_data.get('LNST', np.nan))
            else:
                doanh_thu_raw = loi_nhuan_raw = np.nan
                
            # Lấy Chỉ số Ratios
            if not ratio_y.empty:
                roe_raw = ratio_y.iloc[0].get('ROE', np.nan)
                pe_raw = ratio_y.iloc[0].get('PE', np.nan)
                dar_raw = ratio_y.iloc[0].get('DAR', np.nan) # Nợ/Tài sản
            else:
                roe_raw = pe_raw = dar_raw = np.nan

            # --- ĐƯA VÀO BẢNG HIỂN THỊ ---
            display_data.append({
                "Mã CK": sym,
                "Ngành/Thuộc tính": tag,
                "Sức mạnh": power,
                "Doanh Thu Thuần": format_currency(doanh_thu_raw),
                "Lợi Nhuận ST": format_currency(loi_nhuan_raw),
                "ROE (%)": format_ratio(roe_raw),
                "P/E": format_ratio(pe_raw),
                "Nợ/Tài sản (%)": format_ratio(dar_raw)
            })
            
            # --- ĐƯA VÀO PROMPT CHO LLM ---
            finance_prompt_context += f"\n▶ **{sym}** | Ngành: {tag} | Quyền lực dòng tiền: {power:.2f}\n"
            finance_prompt_context += f"   - Kinh doanh: Doanh thu {format_currency(doanh_thu_raw)} | Lợi nhuận {format_currency(loi_nhuan_raw)}\n"
            finance_prompt_context += f"   - Chỉ số: ROE {format_ratio(roe_raw)}% | P/E {format_ratio(pe_raw)} | Nợ/Tài sản {format_ratio(dar_raw)}%\n"

        # Hiển thị DataFrame
        df_display = pd.DataFrame(display_data).sort_values(by="Sức mạnh", ascending=False)
        st.dataframe(
            df_display, 
            hide_index=True, 
            use_container_width=True,
            column_config={
                "Sức mạnh": st.column_config.ProgressColumn("Quyền lực Network", min_value=0, max_value=1.0, format="%.2f")
            }
        )
        
        # ==========================================
        # NÚT BẤM GỌI AI PHÂN TÍCH
        # ==========================================
        if st.button(f"🧠 Gọi AI Mổ Xẻ Hệ Sinh Thái Băng Đảng {leader}", key=f"btn_{leader}"):
            if not api_key:
                st.error("⚠️ Vui lòng nhập API Key ở Sidebar!")
            else:
                with st.spinner(f"Đang phân tích bộ gen tài chính của băng đảng {leader}..."):
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-flash-latest')
                    
                    prompt = f"""
                    Bạn là Giám đốc Đầu tư (CIO) chuyên phân tích định lượng (Quant) và cơ bản (Fundamental).
                    Nhiệm vụ: Mổ xẻ cấu trúc nội bộ của BĂNG ĐẢNG do '{leader}' dẫn dắt trong NĂM {selected_year}.
                    Ngành chi phối nhóm này là: {dom_sector}.
                    
                    DỮ LIỆU TÀI CHÍNH VÀ QUYỀN LỰC CỦA TỪNG THÀNH VIÊN:
                    {finance_prompt_context}
                    
                    YÊU CẦU ĐẦU RA (Định dạng Markdown):
                    1. **Đánh giá Thủ lĩnh ({leader}):** Sức khỏe tài chính (Doanh thu, Lợi nhuận, ROE) của mã này có đủ mạnh để xứng đáng làm thủ lĩnh hút dòng tiền không, hay chỉ do đầu cơ?
                    2. **Giải mã Kẻ Ngoại Đạo:** Phân tích sâu các mã có Tag '🔥 Ngoại đạo'. Dựa vào cấu trúc nợ (Nợ/Tài sản), ROE hoặc Doanh thu, giải thích TẠI SAO giá cổ phiếu của chúng lại đi theo ngành {dom_sector}? (Gợi ý: Do vay nợ chéo, cộng sinh dự án, v.v.).
                    3. **Rủi ro rạn nứt:** Với bộ chỉ số này, nếu kinh tế xấu đi, mã nào trong băng đảng có nguy cơ "gãy" đầu tiên (Nợ cao, P/E ảo, lỗ)?
                    """
                    
                    try:
                        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.4))
                        st.info("💡 **GÓC NHÌN TỪ SỨ GIẢ AI (GEMINI):**")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Lỗi kết nối AI: {e}")