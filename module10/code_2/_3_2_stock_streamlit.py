
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
from networkx.algorithms import community
# ==========================================
# 1. CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(page_title="iruKa: The Life Simulator", layout="wide", page_icon="🐬")
st.title("🐬 iruKa: Hệ Sinh Thái Đại Dương Tài Chính")
st.markdown("---")

# ==========================================
# 2. HÀM TẠO DỮ LIỆU GIẢ LẬP (MOCK DATA)
# ĐỂ CHẠY WEB NHANH MÀ KHÔNG CẦN CRAWL LẠI
# (Trong thực tế, bạn sẽ load file price_matrix.parquet vào đây)
# ==========================================
@st.cache_data
def load_mock_data():
    # Giả lập ma trận giá của 50 mã trong 10 năm (2500 ngày)
    dates = pd.date_range(start='2014-01-01', periods=2500, freq='B')
    symbols = ['VCB', 'BID', 'CTG', 'MBB', 'TCB', 'VPB', 'SSI', 'VND', 'VCI', 'HCM', 
               'HPG', 'HSG', 'NKG', 'VIC', 'VHM', 'VRE', 'NVL', 'PDR', 'DIG', 'CEO',
               'GAS', 'PVD', 'PVS', 'BSR', 'PLX', 'FPT', 'MWG', 'PNJ', 'MSN', 'VNM',
               'HAH', 'VSC', 'GMD', 'KBC', 'IDC', 'SZC', 'VGC', 'DGC', 'DCM', 'DPM',
               'SAB', 'BHN', 'VJC', 'HVN', 'REE', 'GEX', 'POW', 'NT2', 'HAG', 'DBC']
    
    # Random walk sinh giá
    np.random.seed(42)
    returns = np.random.normal(0.0005, 0.02, size=(2500, 50))
    # Tạo hiệu ứng Burst (Khủng hoảng giả lập vào ngày thứ 1500)
    returns[1480:1520, :] -= 0.05 
    
    price_matrix = pd.DataFrame(returns, index=dates, columns=symbols)
    # Cộng dồn (cumprod) để ra biểu đồ giá
    price_matrix = (1 + price_matrix).cumprod() * 10 
    return price_matrix

price_matrix = load_mock_data()

# ==========================================
# 3. SIDEBAR: CỖ MÁY THỜI GIAN & ĐIỀU KHIỂN
# ==========================================
with st.sidebar:
    st.header("⏱️ Cỗ Máy Thời Gian")
    st.markdown("Kéo thanh trượt để du hành thời gian và quan sát sự dịch chuyển của các băng đảng.")
    
    # Lấy danh sách các năm có trong dữ liệu
    years = sorted(list(set(price_matrix.index.year)))
    selected_year = st.slider("Chọn Năm Quan Sát:", min_value=min(years), max_value=max(years), value=2021)
    
    st.markdown("---")
    st.header("🎮 State Machine: Hành Động")
    st.markdown("Thị trường đang có biến! Bạn chọn gì?")
    action = st.radio("Quyết định Sinh Tử:", 
                      ["Khoanh tay đứng nhìn (Hold)", 
                       "Bán tháo hoảng loạn (Panic Sell)", 
                       "Bắt đáy băng đảng (Bottom Fishing)"])
    
    if st.button("Xác nhận Quyết Định"):
        st.success(f"Hệ thống đã ghi nhận: {action}! Vui lòng chờ xem kết quả ở Quý sau.")

# Lọc dữ liệu theo năm user chọn
df_year = price_matrix[price_matrix.index.year == selected_year]

# ==========================================
# 4. TÍNH TOÁN NETWORK GRAPH (Dành riêng cho Năm được chọn)
# ==========================================
returns_year = df_year.pct_change().dropna()
corr_matrix = returns_year.corr()
distance_matrix = np.sqrt(2 * (1 - corr_matrix))

G = nx.Graph()
stocks = distance_matrix.columns
for i in range(len(stocks)):
    for j in range(i + 1, len(stocks)):
        weight = distance_matrix.iloc[i, j]
        if not np.isnan(weight):
            G.add_edge(stocks[i], stocks[j], weight=weight)
            
mst = nx.minimum_spanning_tree(G)

# Phân cụm AI
communities = list(community.greedy_modularity_communities(mst))
color_palette = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0']
color_map = {}
for i, comm in enumerate(communities):
    for node in comm:
        color_map[node] = color_palette[i % len(color_palette)]


# ==========================================
# 5. VẼ ĐỒ THỊ BONG BÓNG BẰNG PLOTLY (Tương tác được)
# ==========================================
pos = nx.kamada_kawai_layout(mst)

edge_x = []
edge_y = []
for edge in mst.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

node_x = []
node_y = []
node_text = []
node_color = []
node_size = []
centrality = nx.degree_centrality(mst)

for node in mst.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(f"<b>{node}</b>")
    node_color.append(color_map[node])
    # Kích thước node tỷ lệ với độ trung tâm (quyền lực)
    node_size.append(centrality[node] * 300 + 10) 

node_trace = go.Scatter(
    x=node_x, y=node_y, mode='markers+text', text=node_text, textposition="top center",
    hoverinfo='text', marker=dict(color=node_color, size=node_size, line_width=2))

fig_graph = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title=dict(text=f'Bản Đồ Băng Đảng (Năm {selected_year})', font=dict(size=16)),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
             )

# # ==========================================
# # 6. HIỂN THỊ LÊN GIAO DIỆN (MAIN PANEL)
# # ==========================================
col1, col2 = st.columns([2, 1]) # Chia cột: Đồ thị chiếm 2/3, Text chiếm 1/3

with col1:
    # Hiển thị biểu đồ Plotly (Bạn có thể dùng chuột zoom, kéo thả)
    st.plotly_chart(fig_graph, use_container_width=True)
    
    # Hiển thị cái biểu đồ Báo động đỏ (Burst) của năm đó
    st.subheader(f"📊 Chỉ số Căng thẳng Hệ thống (Đường màu đỏ lao dốc là Khủng hoảng)")
    st.line_chart(df_year.mean(axis=1)) # Vẽ tạm chart trung bình giá làm minh họa

with col2:
    st.subheader("🕵️‍♂️ Hồ Sơ AI Storytelling")
    st.info("Nhấp vào các bong bóng bên cạnh để xem ai là Đại ca của mạng lưới. Những bong bóng cùng màu đang bị thao túng bởi cùng một dòng tiền ngầm.")
    
    # Ở đây thay vì gọi lại LLM tốn thời gian, bạn có thể Paste nguyên cái kết quả AI lúc nãy vào
    st.markdown("""
    **🔥 Băng Đảng Đang Chú Ý:**
    
    * **Thủ lĩnh:** CEO (BĐS)
    * **Kẻ ngoại đạo:** EIB (Bank)
    * **Insight:** Trạm trung chuyển vốn ngầm cho các đại gia BĐS phía Nam. Khi Thủ lĩnh CEO "phất cờ", cả băng đảng sẽ tạo ra một cơn sóng đầu cơ cực lớn.
    """)
    
    st.markdown("""
    * **Thủ lĩnh:** CTG (Bank)
    * **Kẻ ngoại đạo:** VIC, VHM (BĐS)
    * **Insight:** "Chính phủ ngầm" của VN-Index. Vingroup cung cấp vốn hóa khổng lồ để điều phối điểm số.
    """)


