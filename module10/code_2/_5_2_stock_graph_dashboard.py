import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px


# ==========================================
# 1. CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(page_title="iruKa: Life Simulator", layout="wide", page_icon="🐬")
st.title("🐬 iruKa: Hệ Sinh Thái Đại Dương Tài Chính 3D")
st.markdown("---")

# ==========================================
# 2. LOAD DỮ LIỆU TỪ DATABASE
# ==========================================
@st.cache_data
def load_databases():
    # Load 3 file CSV bạn vừa tạo ở bước trước
    try:
        df_macro = pd.read_csv("db_macro_network.csv")
        df_meso = pd.read_csv("db_meso_community.csv")
        df_micro = pd.read_csv("db_micro_nodes.csv")
        price_matrix = pd.read_csv("master_price_matrix.csv", index_col=0, parse_dates=True)
        return df_macro, df_meso, df_micro, price_matrix
    except Exception as e:
        st.error("⚠️ Không tìm thấy Database. Hãy chắc chắn bạn đã chạy file bóc tách dữ liệu!")
        st.stop()

df_macro, df_meso, df_micro, price_matrix = load_databases()

# ==========================================
# 3. SIDEBAR: CỖ MÁY THỜI GIAN
# ==========================================
with st.sidebar:
    st.header("⏱️ Cỗ Máy Thời Gian")
    years = sorted(df_macro['Year'].unique())
    selected_year = st.slider("Chọn Năm Quan Sát:", min_value=min(years), max_value=max(years), value=years[-1])
    
    st.markdown("---")
    st.header("🎮 Máy Trạng Thái (XState)")
    st.markdown("Thị trường đang có biến! Bạn chọn gì?")
    action = st.radio("Quyết định Sinh Tử:", 
                      ["Hold (Kim cương)", 
                       "Panic Sell (Bán tháo)", 
                       "Bottom Fishing (Bắt đáy)"])
    if st.button("Xác nhận Quyết Định"):
        st.success(f"Ghi nhận vị thế: {action}. Hệ thống đang giả lập kết quả...")

# ==========================================
# 4. CHIA TAB GIAO DIỆN CHÍNH
# ==========================================
tab1, tab2 = st.tabs(["🌐 BẢN ĐỒ VĨ MÔ (MACRO)", "🔍 KÍNH LÚP CỔ PHIẾU (MICRO)"])

# ---------------------------------------------------------
# TAB 1: BẢN ĐỒ VĨ MÔ & MẠNG LƯỚI
# ---------------------------------------------------------
with tab1:
    col_chart, col_info = st.columns([2, 1])
    
    with col_chart:
        # Tính toán nhanh đồ thị Network cho năm được chọn để lấy tọa độ vẽ
        df_year = price_matrix[price_matrix.index.year == selected_year].dropna(axis=1, thresh=150)
        returns = df_year.pct_change().dropna()
        dist = np.sqrt(2 * (1 - returns.corr()))
        
        G = nx.Graph()
        stocks = dist.columns
        for i in range(len(stocks)):
            for j in range(i + 1, len(stocks)):
                w = dist.iloc[i, j]
                if not np.isnan(w): G.add_edge(stocks[i], stocks[j], weight=w)
        mst = nx.minimum_spanning_tree(G)
        
        # Vẽ Network bằng Plotly
        pos = nx.kamada_kawai_layout(mst)
        edge_x, edge_y = [], []
        for edge in mst.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None]); edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), mode='lines', hoverinfo='none')

        # Lấy data Micro của năm hiện tại
        micro_year = df_micro[df_micro['Year'] == selected_year].set_index('Symbol')
        
        node_x, node_y, node_text, node_size, node_color = [], [], [], [], []
        colors = px.colors.qualitative.Plotly # Bảng màu
        
        for node in mst.nodes():
            node_x.append(pos[node][0])
            node_y.append(pos[node][1])
            node_text.append(f"<b>{node}</b>")
            
            # Size dựa vào Quyền lực (Power_Score)
            if node in micro_year.index:
                node_size.append(micro_year.loc[node, 'Power_Score'] * 400 + 10)
                # Dùng tên thủ lĩnh để gán màu (Các mã chung thủ lĩnh sẽ chung màu)
                leader = micro_year.loc[node, 'Community_Leader']
                node_color.append(colors[abs(hash(leader)) % len(colors)])
            else:
                node_size.append(15); node_color.append('gray')

        node_trace = go.Scatter(
            x=node_x, y=node_y, mode='markers+text', text=node_text, textposition="top center",
            marker=dict(color=node_color, size=node_size, line_width=1, line_color='white'), hoverinfo='text')

        fig_net = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title=dict(text=f'Cấu Trúc Băng Đảng Năm {selected_year}', font=dict(size=18)),
                        showlegend=False, hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        st.plotly_chart(fig_net, use_container_width=True)

    with col_info:
        st.subheader("Bảng Chỉ Huy Vĩ Mô")
        macro_info = df_macro[df_macro['Year'] == selected_year].iloc[0]
        
        # Chỉ báo BURST (Màu đỏ nếu mạng lưới co rút < 30)
        mst_len = macro_info['MST_Length']
        status = "🔴 BURST (Hoảng loạn)" if mst_len < 30 else "🟢 FLOW (Phân hóa ổn định)"
        
        st.metric(label="Tổng chiều dài mạng lưới (MST)", value=mst_len, delta=status, delta_color="off" if mst_len < 30 else "normal")
        st.metric(label="Lãnh chúa Hệ thống", value=macro_info['Market_King'])
        st.metric(label="Số lượng Băng đảng", value=macro_info['Num_Communities'])
        st.metric(label="Hiệu suất TT chung", value=f"{macro_info['Avg_Market_Return']:.2f}%")
        
        st.markdown("---")
        st.markdown("### 📊 Biểu Đồ Sức Khỏe Lịch Sử")
        # Vẽ biểu đồ đường cho thấy MST Length 10 năm
        fig_macro = px.line(df_macro, x='Year', y='MST_Length', markers=True, title="Độ co giãn thị trường (10 năm)")
        fig_macro.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Ngưỡng Khủng Hoảng (Burst)")
        st.plotly_chart(fig_macro, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: KÍNH LÚP CỔ PHIẾU (STOCK X-RAY)
# ---------------------------------------------------------
with tab2:
    st.markdown("### 🕵️‍♂️ Hồ Sơ Tội Phạm Tài Chính")
    st.write("Tra cứu lịch sử quyền lực và sự phản bội băng đảng của một mã chứng khoán bất kỳ qua 10 năm.")
    
    all_symbols = sorted(df_micro['Symbol'].unique())
    target_stock = st.selectbox("Chọn Mã Cổ Phiếu để X-Ray:", all_symbols, index=all_symbols.index('MWG') if 'MWG' in all_symbols else 0)
    
    # Lọc data của mã này
    stock_history = df_micro[df_micro['Symbol'] == target_stock].sort_values('Year')
    
    col_chart2, col_table2 = st.columns([2, 1])
    
    with col_chart2:
        # Biểu đồ Quỹ đạo Quyền lực (Ranking)
        # Lộn ngược trục Y để Rank 1 ở trên cùng
        fig_rank = px.line(stock_history, x='Year', y='Power_Rank', markers=True, 
                           title=f"Quỹ Đạo Quyền Lực của {target_stock} (Rank càng nhỏ càng mạnh)",
                           labels={'Power_Rank': 'Xếp hạng Quyền lực'})
        fig_rank.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_rank, use_container_width=True)

    with col_table2:
        st.markdown(f"**Lịch sử Băng đảng của {target_stock}**")
        # Bảng hiển thị năm nào theo Đại ca nào
        display_df = stock_history[['Year', 'Community_Leader', 'Power_Rank', 'Yearly_Return']].copy()
        display_df.columns = ['Năm', 'Đại ca dẫn dắt', 'Hạng', 'Lợi nhuận (%)']
        st.dataframe(display_df, hide_index=True)
