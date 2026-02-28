# 📋 KẾ HOẠCH TRIỂN KHAI GIAI ĐOẠN 4: PHÂN TÍCH ĐỘNG LỰC HỌC THỊ TRƯỜNG VÀ HÀNH VI GIAO DỊCH (52-WEEK MARKET DYNAMICS)

## 1. MỤC TIÊU GIAI ĐOẠN (PHASE OBJECTIVE)

Tích hợp dữ liệu chuỗi thời gian (Time-series data) về Giá và Khối lượng giao dịch của 52 tuần trong năm nhằm đối chiếu với Báo cáo tài chính (Fundamental) và Cấu trúc Mạng lưới (Network).
Mục tiêu cốt lõi là nhận diện sự phân kỳ giữa hiệu quả kinh doanh thực tế và hành vi giao dịch trên thị trường, từ đó phát hiện các dấu hiệu bất thường về thanh khoản hoặc biến động giá.

---

## 2. PHÂN HỆ XỬ LÝ DỮ LIỆU (ETL PIPELINE - `build_market_dynamics.py`)

Tiến hành xây dựng script đọc dữ liệu giao dịch hàng ngày (Daily Trading Data) từ cơ sở dữ liệu gốc và thực hiện gom nhóm (Resampling) theo chu kỳ Tuần (Weekly).

Dữ liệu đầu ra cần được trích xuất thành 2 định dạng phục vụ cho UI và AI:

### 2.1. Dữ liệu mảng chuỗi thời gian (Time-series Array)

* **Tính toán:** Thu thập chính xác 52 mức giá đóng cửa (Close Price) của 52 tuần trong năm phân tích.
* **Định dạng:** Lưu trữ dưới dạng danh sách (List/Array) ví dụ: `[10.5, 11.2, ..., 15.0]`.
* **Mục đích:** Cung cấp dữ liệu thô để render biểu đồ thu nhỏ (Sparklines) trực tiếp trên giao diện dạng bảng.

### 2.2. Các Trọng số Hành vi (Behavioral Metrics)

Tính toán các chỉ số thống kê định lượng để đo lường mức độ rủi ro và bất thường của cổ phiếu:

* **Max Drawdown (Độ sụt giảm tối đa):** Đo lường tỷ lệ phần trăm giảm giá sâu nhất từ đỉnh cao nhất (Peak) xuống đáy thấp nhất (Trough) trong vòng 52 tuần. Chỉ số này phản ánh rủi ro sụt giảm vốn.
* **Volatility (Độ biến động):** Đo lường bằng độ lệch chuẩn (Standard Deviation) của lợi nhuận hàng tuần. Phản ánh mức độ dao động giá của tài sản.
* **Volume Spike Weeks (Số tuần đột biến khối lượng):** Thống kê số lượng tuần có khối lượng giao dịch thực tế lớn hơn hoặc bằng 200% (gấp 2 lần) so với khối lượng giao dịch trung bình 52 tuần. Chỉ số này hỗ trợ nhận diện dòng tiền lớn tham gia hoặc rút lui.

---

## 3. NÂNG CẤP GIAO DIỆN STREAMLIT (UI DASHBOARD UPGRADE)

Bổ sung các trường thông tin động lực học vào Bảng dữ liệu (Data Grids) hiện tại thuộc phân hệ "Soi Báo Cáo Tài Chính Nội Bộ Băng Đảng":

* **Cột "Hành trình 52 Tuần":** Tích hợp tính năng `st.column_config.LineChartColumn` của Streamlit để hiển thị biểu đồ đường thu nhỏ (Sparkline) đại diện cho xu hướng giá trong năm, giúp người dùng quan sát trực quan mà không cần mở tab đồ thị rời.
* **Các cột Chỉ số Rủi ro:** Hiển thị cụ thể các giá trị `Max Drawdown (%)`, `Độ biến động`, và `Số tuần đột biến Volume`.

---

## 4. TỐI ƯU HÓA PROMPT CHO LLM (AI INTEGRATION UPGRADE)

Cập nhật ngữ cảnh (Context) và hệ thống câu lệnh (Prompt) gửi tới LLM để AI có khả năng thực hiện Phân tích liên kết (Cross-analysis) giữa 3 trụ cột dữ liệu.

**Ngữ cảnh bổ sung vào Prompt:**

* Cung cấp các trọng số `Max Drawdown`, `Volatility`, và `Volume Spikes` của từng mã cổ phiếu tương ứng với dữ liệu Tài chính (ROE, Lợi nhuận, Nợ) và Mạng lưới (Điểm quyền lực).

**Yêu cầu đầu ra (Output Requirements) đối với LLM:**

1. **Kiểm chứng sự đồng pha:** Đánh giá xem biến động giá và thanh khoản (Volume) có được hậu thuẫn bởi kết quả kinh doanh (Fundamental) hay không.
2. **Nhận diện rủi ro giao dịch:** Chỉ ra các mã có dấu hiệu rủi ro cao dựa trên sự phân kỳ (ví dụ: Lợi nhuận thấp/âm nhưng khối lượng giao dịch đột biến liên tục kèm độ biến động lớn).
3. **Phân tích hành vi dòng tiền:** Đánh giá động thái của dòng tiền đối với các mã "Ngoại đạo" (Spy/Outlier) dựa trên lịch sử 52 tuần giao dịch.