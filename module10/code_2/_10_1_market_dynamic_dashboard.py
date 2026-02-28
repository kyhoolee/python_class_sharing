import streamlit as st
import pandas as pd
import numpy as np
import json
import google.generativeai as genai

st.set_page_config(page_title="iruKa: The Holy Trinity", layout="wide", page_icon="🧿")
st.title("🧿 iruKa: Tổ hợp 3 Lăng kính (Network + Fundamental + Dynamics)")

# ==========================================
# 1. LOAD TOÀN BỘ 3 TRỤ CỘT DATABASE
# ==========================================
@st.cache_data
def load_all_data():
    df_meso = pd.read_csv("db_meso_community.csv")
    df_micro = pd.read_csv("db_micro_nodes.csv")
    df_fin_year = pd.read_csv("db_finance_year.csv")
    df_ratios = pd.read_csv("db_finance_ratios.csv")
    df_dynamics = pd.read_csv("db_market_dynamics.csv") 
    
    df_sector = pd.read_csv("db_sector_map.csv")
    sector_map = dict(zip(df_sector['Symbol'], df_sector['Sector']))
    
    return df_meso, df_micro, df_fin_year, df_ratios, df_dynamics, sector_map

df_meso, df_micro, df_fin_year, df_ratios, df_dynamics, SECTOR_MAP = load_all_data()

def format_currency(val):
    try: return "N/A" if pd.isna(val) else f"{float(val) / 1e6:,.1f} Tỷ"
    except: return "N/A"

def format_ratio(val):
    try: return "N/A" if pd.isna(val) else f"{float(val):.2f}"
    except: return "N/A"

# ==========================================
# 2. BẢNG ĐIỀU KHIỂN
# ==========================================
with st.sidebar:
    st.header("⚙️ Bảng Điều Khiển")
    years = sorted(df_micro['Year'].unique())
    selected_year = st.selectbox("Chọn Năm Phân Tích:", years, index=len(years)-1)
    st.markdown("---")
    api_key = st.text_input("🔑 Nhập Gemini API Key:", type="password")

# ==========================================
# 3. CHUẨN BỊ DỮ LIỆU TỔ HỢP 3 TRỤ CỘT
# ==========================================
meso_year = df_meso[df_meso['Year'] == selected_year]
leaders = meso_year['Leader'].tolist()

if not leaders:
    st.warning(f"Không có dữ liệu Băng đảng cho năm {selected_year}.")
    st.stop()

tabs = st.tabs([f"👑 Nhóm {l}" for l in leaders])

for leader, tab in zip(leaders, tabs):
    with tab:
        group_info = meso_year[meso_year['Leader'] == leader].iloc[0]
        members = group_info['Members'].split(', ')
        sectors = [SECTOR_MAP.get(m, 'Khác') for m in members]
        dom_sector = max(set(sectors), key=sectors.count)

        st.markdown(f"### 🛡️ Băng đảng **{leader}** | Ngành chi phối: **{dom_sector}**")
        
        display_data = []
        holy_trinity_context = "" # Biến gom dữ liệu cho AI

        for sym in members:
            # --- TRỤ CỘT 1: NETWORK ---
            sec = SECTOR_MAP.get(sym, 'Khác')
            tag = sec if sec == dom_sector else f"🔥 Ngoại đạo ({sec})"
            power = df_micro[(df_micro['Symbol'] == sym) & (df_micro['Year'] == selected_year)]['Power_Score'].values[0]
            
            # --- TRỤ CỘT 2: FUNDAMENTAL ---
            fin_y = df_fin_year[(df_fin_year['Symbol'] == sym) & (df_fin_year['Nam'] == selected_year)]
            ratio_y = df_ratios[(df_ratios['Symbol'] == sym) & (df_ratios['Nam'] == selected_year)]
            
            if not fin_y.empty:
                row_data = fin_y.iloc[0]
                
                # 1. Lấy Doanh thu: Ưu tiên TotalIncome (Bank), nếu NaN thì lấy DTTBHCCDV (DN thường)
                doanh_thu_raw = row_data.get('TotalIncome', np.nan)
                if pd.isna(doanh_thu_raw):
                    doanh_thu_raw = row_data.get('DTTBHCCDV', np.nan)
                    
                # 2. Lấy Lợi nhuận: Ưu tiên NetIncome, nếu NaN thì lấy LNST
                loi_nhuan_raw = row_data.get('NetIncome', np.nan)
                if pd.isna(loi_nhuan_raw):
                    loi_nhuan_raw = row_data.get('LNST', np.nan)
            else:
                doanh_thu_raw = loi_nhuan_raw = np.nan
                
            roe_raw = ratio_y.iloc[0].get('ROE', np.nan) if not ratio_y.empty else np.nan
            pe_raw = ratio_y.iloc[0].get('PE', np.nan) if not ratio_y.empty else np.nan
            dar_raw = ratio_y.iloc[0].get('DAR', np.nan) if not ratio_y.empty else np.nan # Nợ/Tài sản
            
            # --- TRỤ CỘT 3: MARKET DYNAMICS ---
            dyn_y = df_dynamics[(df_dynamics['Symbol'] == sym) & (df_dynamics['Year'] == selected_year)]
            
            if not dyn_y.empty:
                weekly_list = json.loads(dyn_y.iloc[0]['Weekly_Close_List'])
                max_dd = dyn_y.iloc[0]['Max_Drawdown_%']
                volat = dyn_y.iloc[0]['Volatility_%']
                spikes = dyn_y.iloc[0]['Volume_Spike_Weeks']
            else:
                weekly_list = []
                max_dd = volat = spikes = np.nan

            # --- ĐƯA LÊN BẢNG UI ---
            display_data.append({
                "Mã CK": sym,
                "Thuộc tính": tag,
                "Network (Power)": power,
                "Doanh Thu": format_currency(doanh_thu_raw),
                "Lợi Nhuận": format_currency(loi_nhuan_raw),
                "ROE (%)": format_ratio(roe_raw),
                "Nợ/Tài sản (%)": format_ratio(dar_raw),
                "Đồ thị 52 Tuần": weekly_list,
                "Sập Max (%)": format_ratio(max_dd),
                "Vol Nổ (Tuần)": spikes
            })
            
            # --- BƠM DỮ LIỆU TOÀN DIỆN CHO LLM ---
            holy_trinity_context += f"\n▶ **{sym}** | Ngành: {tag} | Quyền lực Network: {power:.2f}\n"
            holy_trinity_context += f"   - [CƠ BẢN]: Doanh thu {format_currency(doanh_thu_raw)} | Lợi nhuận {format_currency(loi_nhuan_raw)} | ROE {format_ratio(roe_raw)}% | P/E {format_ratio(pe_raw)} | Nợ/Tài sản {format_ratio(dar_raw)}%\n"
            holy_trinity_context += f"   - [HÀNH VI]: Rơi mạnh nhất {format_ratio(max_dd)}% | Độ biến động {format_ratio(volat)}% | Nổ Volume: {spikes} tuần\n"

        # Hiển thị DataFrame
        df_display = pd.DataFrame(display_data).sort_values(by="Network (Power)", ascending=False)
        st.dataframe(
            df_display, 
            hide_index=True, 
            use_container_width=True,
            column_config={
                "Network (Power)": st.column_config.ProgressColumn("Quyền lực Network", min_value=0, max_value=1.0, format="%.2f"),
                "Đồ thị 52 Tuần": st.column_config.LineChartColumn("Giá 52 Tuần", y_min=0),
                "Vol Nổ (Tuần)": st.column_config.NumberColumn("Số tuần nổ Vol", format="%d")
            }
        )
        
        # ==========================================
        # GỌI AI: PHÂN TÍCH TỔ HỢP 3 LĂNG KÍNH
        # ==========================================
        if st.button(f"🧠 Gọi AI Đánh Giá Toàn Diện Băng Đảng {leader}", key=f"btn_trinity_{leader}"):
            if not api_key:
                st.error("⚠️ Vui lòng nhập API Key ở Sidebar!")
            else:
                with st.spinner(f"Đang tổng hợp dữ liệu Network, Cơ Bản và Hành Vi của băng đảng {leader}..."):
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-flash-latest')
                    
                    prompt = f"""
                    Bạn là Giám đốc Đầu tư (CIO) sở hữu góc nhìn đa chiều: Định lượng (Network), Cơ bản (Fundamental) và Hành vi (Price Action).
                    Hãy đánh giá sự sống còn của BĂNG ĐẢNG do '{leader}' dẫn dắt trong NĂM {selected_year}. Ngành chi phối: {dom_sector}.
                    
                    DỮ LIỆU TỔ HỢP 3 TRỤ CỘT:
                    {holy_trinity_context}
                    
                    YÊU CẦU PHÂN TÍCH (Lập luận logic, sắc bén, định dạng Markdown):
                    1. **Đối chiếu Giá trị và Hành vi:** Hãy phân tích sự đồng pha (hoặc phân kỳ) giữa [CƠ BẢN] và [HÀNH VI] của 1-2 mã nổi bật. Ví dụ: Mã có ROE và Lợi nhuận rất tốt nhưng giá lại Sập Max rất sâu và biến động cao -> Điều gì đang xảy ra? Hay mã Lợi nhuận kém, Nợ cao nhưng nổ Volume liên tục -> Đội lái đang kéo xả?
                    2. **Giải mã Network Ngoại Đạo:** Dựa vào [CƠ BẢN] (Đặc biệt là cấu trúc Nợ/Tài sản), tại sao dòng tiền [HÀNH VI] lại ép các mã '🔥 Ngoại đạo' đi chung với băng đảng này? Sự liên kết này là cộng sinh bền vững hay ôm bom nợ chéo?
                    3. **Kết luận Rủi ro Hệ thống:** Tổng duyệt lại toàn bộ băng đảng. Với bộ số liệu HÀNH VI (Độ biến động, Sập) và CƠ BẢN (Nợ, ROE) như trên, băng đảng này đang khỏe mạnh hút tiền thật, hay là một quả bóng đầu cơ chực chờ nổ tung?
                    """
                    
                    try:
                        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.3))
                        st.info("💡 **BÁO CÁO CHIẾN LƯỢC TỔ HỢP TỪ AI:**")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Lỗi kết nối AI: {e}")