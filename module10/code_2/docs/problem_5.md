Dưới đây là Tài liệu Yêu cầu Dự án (PRD - Product Requirements Document) được viết lại theo văn phong khách quan, chuyên nghiệp và chuẩn tính kỹ thuật. Bạn có thể copy toàn bộ nội dung này và lưu thành file `PRD_iruKa_Life_Simulator.md` để làm tài liệu tham khảo cho dự án.

---

# 📋 TÀI LIỆU YÊU CẦU DỰ ÁN (PRD): HỆ THỐNG GIẢ LẬP VÀ PHÂN TÍCH MẠNG LƯỚI TÀI CHÍNH (IRUKA LIFE SIMULATOR)

## 1. TỔNG QUAN DỰ ÁN (PROJECT OVERVIEW)

**Mục tiêu:** Xây dựng một hệ thống giả lập và phân tích thị trường chứng khoán (Dashboard) kết hợp giữa Khoa học Mạng lưới (Network Science) và Trí tuệ Nhân tạo tạo tạo sinh (Generative AI).
Hệ thống không sử dụng các chỉ báo kỹ thuật truyền thống mà đánh giá dòng tiền dựa trên nguyên lý **Econophysics** (Vật lý Kinh tế), tập trung vào 3 trạng thái:

* **Invariant (Bất biến):** Thuộc tính gốc và phân cụm cốt lõi của doanh nghiệp.
* **Flow (Dòng chảy):** Sự dịch chuyển quyền lực và dòng tiền giữa các nhóm cổ phiếu.
* **Burst (Đột biến):** Hiện tượng "Mất bậc tự do" (Mạng lưới co rúm) khi xảy ra hoảng loạn hoặc khủng hoảng hệ thống.

---

## 2. NỀN TẢNG DỮ LIỆU (DATA FOUNDATION)

* **Nguồn dữ liệu:** Lịch sử giá cổ phiếu thị trường Việt Nam trong 10 năm (2015 - 2025) và API Hồ sơ doanh nghiệp (CafeF).
* **Trường dữ liệu cốt lõi:** `GiaDieuChinh` (Giá điều chỉnh) để đảm bảo tính liên tục của chuỗi thời gian.
* **Quy mô phân tích (Universe):** Tập trung vào Top 50 cổ phiếu có thanh khoản cao nhất, đóng vai trò là trục xương sống của hệ thống tài chính.
* **Xử lý điểm mù dữ liệu:** Hệ thống cần có cơ chế linh hoạt loại bỏ các mã chưa niêm yết trong các năm quá khứ (ví dụ: `thresh=150` ngày giao dịch/năm) để đảm bảo tính toàn vẹn của thuật toán.

---

## 3. KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

Hệ thống được chia thành 3 phân hệ (Modules) hoạt động độc lập:

### Phân hệ 3.1: Xử lý Dữ liệu ngầm (ETL Pipeline)

Thực hiện trích xuất, biến đổi chuỗi giá thành dữ liệu không gian và lưu trữ dưới dạng Database (CSV) để tối ưu hóa tốc độ truy xuất. Dữ liệu được bóc tách thành 3 lăng kính:

1. **Macro (Vĩ mô - `db_macro_network.csv`):** Thống kê theo từng năm. Các chỉ số gồm: Tổng chiều dài cây bao trùm (MST Length - dùng để đo lường cảnh báo Burst), Số lượng cụm (Communities), Thủ lĩnh toàn thị trường, Hiệu suất chung.
2. **Meso (Trung mô - `db_meso_community.csv`):** Phân tích cấu trúc nhóm. Các chỉ số gồm: ID Nhóm, Mã định danh Thủ lĩnh, Quy mô nhóm, Danh sách thành viên.
3. **Micro (Vi mô - `db_micro_nodes.csv`):** Hồ sơ từng cổ phiếu. Các chỉ số gồm: Mã CK, Nhóm trực thuộc, Điểm quyền lực (Centrality Score), Thứ hạng quyền lực toàn thị trường, Tỷ suất sinh lời.
4. **Company Profiles (`db_company_profiles.csv`):** Dữ liệu thu thập từ API chứa Tên đầy đủ và Mô tả doanh nghiệp.

### Phân hệ 3.2: Giao diện Người dùng (Dashboard UI/UX)

Sử dụng Streamlit để xây dựng giao diện tập trung vào việc **hiển thị dữ liệu có cấu trúc (Structured Data Grids)** thay vì đồ thị Node-Edge tĩnh.

* **Cỗ máy thời gian (Sidebar):** Thanh điều hướng cho phép chọn năm phân tích.
* **Bảng Chỉ huy Vĩ mô:** Hiển thị các Metric cốt lõi (Tổng chiều dài MST, Cảnh báo trạng thái Hoảng loạn/Phân hóa).
* **Danh sách Cấu trúc Quyền lực (Main Panel):** * Trình bày dưới dạng các Khung mở rộng (Expander) phân theo Nhóm/Thủ lĩnh.
* Trong mỗi nhóm, danh sách cổ phiếu được hiển thị dưới dạng **Bảng (Table)**, sắp xếp thứ tự từ mạnh đến yếu dựa trên Điểm quyền lực.
* Tích hợp thanh biểu đồ (Progress Bar in-cell) trực quan hóa độ lớn quyền lực.
* Hiển thị cảnh báo trực quan (Tags) đối với các mã "Ngoại đạo" (Cổ phiếu đi chệch khỏi nhóm ngành gốc).



### Phân hệ 3.3: Tích hợp AI Phân tích (LLM Agent)

Sử dụng LLM (khuyến nghị Google Gemini 1.5 Flash) để tự động hóa việc đọc hiểu dữ liệu và kết xuất báo cáo tình báo tài chính.

* **Cơ chế:** Ghép nối dữ liệu cấu trúc (Bảng Vi mô/Trung mô) của một năm cụ thể thành chuỗi văn bản (Prompt). Đưa kèm các thông tin về Tên công ty, Ngành nghề gốc, Mã Thủ lĩnh và Điểm sức mạnh.
* **Yêu cầu Đầu ra:** Cung cấp báo cáo giải thích tính hợp lý/bất hợp lý của cấu trúc dòng tiền năm đó, mổ xẻ nguyên nhân các mã "Ngoại đạo" di cư sang nhóm khác (nhấn mạnh vào quan hệ cộng sinh tài chính ngầm).

---

## 4. QUY TRÌNH THỰC THI CHUẨN (IMPLEMENTATION ROADMAP)

* **Giai đoạn 1: Chuẩn bị Dữ liệu (Data Preparation)**
* Chạy kịch bản tổng hợp giá 50 mã chứng khoán ra file `master_price_matrix.csv`.
* Khởi chạy kịch bản Crawler API để thu thập thông tin doanh nghiệp, xuất ra file `db_company_profiles.csv`.


* **Giai đoạn 2: Xây dựng Cơ sở dữ liệu Mạng lưới (Network Database Generation)**
* Viết script chạy vòng lặp theo từng năm. Biến đổi Tương quan (Correlation) thành Khoảng cách (Euclidean Distance), tính toán Cây bao trùm nhỏ nhất (MST) và phân cụm (Community Detection).
* Trích xuất các hệ số Centrality và xuất ra 3 file CSV (`macro`, `meso`, `micro`).


* **Giai đoạn 3: Phát triển Giao diện (Streamlit Dashboard)**
* Nạp 4 file CSV (3 file Network + 1 file Profile) vào bộ nhớ đệm (Cache).
* Xây dựng UI dạng Bảng (Data Grids) sử dụng `st.column_config` để trực quan hóa dữ liệu.


* **Giai đoạn 4: Tích hợp AI (LLM Integration)**
* Xây dựng Module gửi Prompt động dựa trên năm được chọn.
* Hiển thị kết quả "Biên niên sử" hoặc "Báo cáo thường niên" ngay trên giao diện Streamlit.