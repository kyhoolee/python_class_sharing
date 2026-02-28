import streamlit as st
import pandas as pd
import google.generativeai as genai

# ==========================================
# 1. CẤU HÌNH & TỪ ĐIỂN NGÀNH NGHỀ
# ==========================================
st.set_page_config(page_title="iruKa: Life Simulator", layout="wide", page_icon="🐬")



# ==========================================
# 2. LOAD DATABASE (Cập nhật thêm file Sector)
# ==========================================
@st.cache_data
def load_databases():
    try:
        df_macro = pd.read_csv("db_macro_network.csv")
        df_meso = pd.read_csv("db_meso_community.csv")
        df_micro = pd.read_csv("db_micro_nodes.csv")
        df_profiles = pd.read_csv("db_company_profiles.csv")
        price_matrix = pd.read_csv("master_price_matrix.csv", index_col=0, parse_dates=True)
        
        # ĐỌC TỪ ĐIỂN NGÀNH NGHỀ ĐỘNG TỪ FILE
        df_sector = pd.read_csv("db_sector_map.csv")
        # Chuyển DataFrame thành Dictionary: {'VCB': 'TaiChinh', 'HPG': 'NguyenVatLieu'...}
        sector_map_dict = dict(zip(df_sector['Symbol'], df_sector['Sector']))
        
        return df_macro, df_meso, df_micro, df_profiles, price_matrix, sector_map_dict
        
    except Exception as e:
        st.error(f"⚠️ Lỗi Load Database: {e}")
        st.stop()

# Nhận biến SECTOR_MAP tự động từ hàm load
df_macro, df_meso, df_micro, df_profiles, price_matrix, SECTOR_MAP = load_databases()


# ==========================================
# 3. SIDEBAR: CỖ MÁY THỜI GIAN
# ==========================================
with st.sidebar:
    st.header("⏱️ Trục Thời Gian")
    years = sorted(df_macro['Year'].unique())
    selected_year = st.slider("Chọn Năm Phân Tích:", min_value=min(years), max_value=max(years), value=years[-1])
    
    st.markdown("---")
    st.header("🔑 Cấu hình AI")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")

# ==========================================
# 4. GIAO DIỆN CHÍNH (MAIN DASHBOARD)
# ==========================================
st.title(f"📊 CẤU TRÚC QUYỀN LỰC DÒNG TIỀN NĂM {selected_year}")

macro_info = df_macro[df_macro['Year'] == selected_year].iloc[0]
mst_len = macro_info['MST_Length']
is_burst = mst_len < 30

# Thẻ trạng thái vĩ mô
col1, col2, col3, col4 = st.columns(4)
col1.metric("Chiều dài Mạng lưới (Sức khỏe)", f"{mst_len}", delta="BURST (Hoảng loạn)" if is_burst else "FLOW (Phân hóa)", delta_color="inverse" if is_burst else "normal")
col2.metric("Lãnh chúa Thị trường", macro_info['Market_King'])
col3.metric("Số lượng Băng đảng", macro_info['Num_Communities'])
col4.metric("Hiệu suất VN-Index", f"{macro_info['Avg_Market_Return'] * 100:.2f}%")
st.markdown("---")

# ==========================================
# 5. RENDER BẢNG DỮ LIỆU CÓ CẤU TRÚC (DATA GRIDS)
# ==========================================
meso_year = df_meso[df_meso['Year'] == selected_year]
micro_year = df_micro[df_micro['Year'] == selected_year]

# Tạo biến lưu trữ string để gửi cho LLM sau này
llm_context_data = ""

for _, row in meso_year.iterrows():
    leader = row['Leader']
    members = row['Members'].split(', ')
    
    # 5.1. Phân tích Ngành thống trị và Ngoại đạo
    sectors = [SECTOR_MAP.get(m, 'Khác') for m in members]
    dominant_sector = max(set(sectors), key=sectors.count)
    
    # 5.2. Lọc Micro data cho nhóm này, gộp với Profile và sort theo sức mạnh
    group_df = micro_year[micro_year['Symbol'].isin(members)].copy()
    group_df = pd.merge(group_df, df_profiles[['Symbol', 'Company_Name', 'Description']], on='Symbol', how='left')
    group_df = group_df.sort_values(by='Power_Score', ascending=False)
    
    # Tạo cột Tag
    def get_tag(sym):
        sec = SECTOR_MAP.get(sym, 'Khác')
        return sec if sec == dominant_sector else f"🔥 Ngoại đạo ({sec})"
    group_df['Tag'] = group_df['Symbol'].apply(get_tag)
    
    # Đưa vào Context cho LLM
    llm_context_data += f"\n🛡️ BĂNG ĐẢNG {leader} (Ngành chi phối: {dominant_sector})\n"
    for _, m_row in group_df.iterrows():
        llm_context_data += f" - {m_row['Symbol']} ({m_row['Company_Name']}) | Tag: {m_row['Tag']} | Điểm quyền lực: {m_row['Power_Score']:.2f}\n"

    # 5.3. Trực quan hóa bằng Expander & Column Config
    with st.expander(f"👑 BĂNG ĐẢNG: {leader} | Ngành: {dominant_sector} | Thành viên: {len(members)} mã", expanded=True):
        
        display_df = group_df[['Symbol', 'Company_Name', 'Tag', 'Power_Score', 'Yearly_Return']]
        display_df['Yearly_Return'] = display_df['Yearly_Return'] * 100
        
        st.dataframe(
            display_df,
            column_config={
                "Symbol": st.column_config.TextColumn("Mã CK", width="small"),
                "Company_Name": st.column_config.TextColumn("Tên Công Ty", width="medium"),
                "Tag": st.column_config.TextColumn("Thuộc tính", width="small"),
                "Power_Score": st.column_config.ProgressColumn(
                    "Sức mạnh (Độ trung tâm)",
                    help="Thanh Bar hiển thị quyền lực trong nhóm",
                    format="%.2f",
                    min_value=0,
                    max_value=float(micro_year['Power_Score'].max()), # Scale theo người mạnh nhất năm
                ),
                "Yearly_Return": st.column_config.NumberColumn(
                    "Hiệu suất năm %",
                    format="%+.2f %%",
                )
            },
            hide_index=True,
            use_container_width=True
        )

# ==========================================
# 6. GỌI LLM PHÂN TÍCH CHUYÊN SÂU
# ==========================================
st.markdown("---")
st.header("🧠 BÁO CÁO TÌNH BÁO AI (MICRO-ANALYSIS)")

if st.button(f"Phân tích chuyên sâu cấu trúc Năm {selected_year}"):
    if not api_key:
        st.warning("Vui lòng nhập Gemini API Key ở thanh công cụ bên trái!")
    else:
        with st.spinner("Sứ giả AI đang soi cấu trúc các băng đảng..."):
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')
            
            prompt = f"""
            Bạn là một chuyên gia Tình báo Tài chính & Econophysics sắc sảo.
            Dưới đây là sơ đồ cấu trúc các Băng đảng Cổ phiếu trên sàn chứng khoán VN NĂM {selected_year}.
            
            BỐI CẢNH VĨ MÔ NĂM {selected_year}:
            - Mạng lưới đang ở trạng thái: {'HOẢNG LOẠN CO RÚM (Burst)' if is_burst else 'PHÂN HÓA ỔN ĐỊNH (Flow)'}.
            
            CẤU TRÚC CHI TIẾT (Đã xếp từ mạnh đến yếu):
            {llm_context_data}
            
            YÊU CẦU ĐẦU RA (Viết dạng Markdown, ngôn ngữ lôi cuốn, kịch tính):
            1. Tóm tắt bối cảnh dòng tiền năm {selected_year}. Trạng thái vĩ mô đang chi phối hành vi các mã như thế nào?
            2. Đi sâu vào 2-3 Băng đảng quan trọng nhất. Phân tích TẠI SAO các mã có Tag '🔥 Ngoại đạo' lại nằm trong nhóm đó? (Ví dụ: Sự cộng sinh ngầm, vay nợ, hoặc bám đuôi dòng tiền).
            3. Nhận xét về vị thế của kẻ cầm đầu (Leader) trong năm nay.
            """
            
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(max_output_tokens=4096, temperature=0.7)
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Lỗi khi gọi API: {e}")