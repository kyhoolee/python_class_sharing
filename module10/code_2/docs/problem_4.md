# 📋 ĐỀ BÀI DỰ ÁN: XÂY DỰNG HỆ SINH THÁI ĐẠI DƯƠNG TÀI CHÍNH 3D (IRUKA LIFE SIMULATOR)

**Mục tiêu:** Xây dựng một Dashboard giả lập (Simulator) kết hợp Khoa học Mạng lưới (Network Science) và Trí tuệ Nhân tạo (LLM) để trực quan hóa lịch sử 10 năm của thị trường chứng khoán Việt Nam. Thông qua đó, người học rèn luyện tư duy hệ thống và kỹ năng quản trị rủi ro theo triết lý **iruKa: Invariant (Bất biến) - Flow (Dòng chảy) - Burst (Đột biến)**.

---

## 1. NỀN TẢNG DỮ LIỆU (DATA FOUNDATION)

Thay vì phân tích toàn bộ 1500 mã nhiễu loạn, hệ thống chỉ tập trung vào "Tinh hoa" của thị trường.

* **Nguồn dữ liệu:** Lịch sử giá 10 năm (2015 - 2025) từ CafeF.
* **Trường dữ liệu lõi:** `GiaDieuChinh` (để đảm bảo tính liên tục của tài sản).
* **Universe (Vũ trụ quan sát):** **Top 50 mã chứng khoán** có thanh khoản cao nhất và lịch sử sinh tồn lâu nhất (Đã được lọc qua thuật toán Survivorship Bias).

---

## 2. KIẾN TRÚC THUẬT TOÁN 3 CHIỀU (3D TEMPORAL NETWORK)

Hệ thống không nhìn thị trường như một biểu đồ 2D phẳng, mà là một **Thước phim không gian 3 chiều (Node - Edge - Time)**.

### A. Tầng INVARIANT: Gắn "Hộ Khẩu" Băng Đảng (Master Backbone)

* **Toán học:** Tính ma trận tương quan  và khoảng cách hình học  trên toàn bộ tập dữ liệu 10 năm. Dựng Cây bao trùm nhỏ nhất (MST).
* **Nhiệm vụ AI:** Sử dụng thuật toán `Community Detection` để chia 50 mã thành các "Băng đảng" gốc.
* **Kết quả:** Cố định MÀU SẮC của từng node. *(Ví dụ: HPG vĩnh viễn mang màu của băng đảng Thép/Tài chính, dù các năm sau nó có trôi dạt đi đâu).*

### B. Tầng FLOW: Động Lực Học Mạng Lưới Qua Từng Năm

* **Toán học:** Trượt trục thời gian  theo từng năm. Tính lại ma trận khoảng cách và MST cho riêng năm đó.
* **Hiện tượng quan sát:** * *Quỹ đạo Quyền lực:* Node nào có độ trung tâm (Centrality) cao nhất năm đó sẽ phình to ra (Thủ lĩnh dòng tiền).
* *Sự di cư:* Các node (mặc dù cố định màu sắc gốc) sẽ dịch chuyển lại gần hoặc văng ra xa khỏi thủ lĩnh tùy thuộc vào dòng tiền năm đó.



### C. Tầng BURST: Đo lường Sức Khỏe Hệ Thống & Rủi Ro Đuôi Béo

* **Toán học:** Tính tổng chiều dài của Cây bao trùm () của từng năm/quý.
* **Hiện tượng quan sát:** Khi tổng chiều dài này co rút đột ngột (khoảng cách tiến về 0), báo hiệu toàn bộ thị trường đang hoảng loạn (Tương quan tiến về 1, mọi thứ đều bị bán tháo). Đây là **Báo động Đỏ (Khủng hoảng)**.

---

## 3. TÍCH HỢP AI TRẦN THUẬT (LLM CHRONICLE STORYTELLING)

Thay vì phân tích tĩnh từng năm, hệ thống sẽ tổng hợp Dữ liệu Chuỗi thời gian (Time-series metadata) để "mớm" cho LLM (Google Gemini).

* **Input (Prompt):** Bức tranh cấu trúc quyền lực tịnh tiến từ năm 1 đến năm 10 (Gồm: Ai là thủ lĩnh mỗi năm? Năm nào có Burst co rúm mạng lưới? Mã ngoại đạo nào đổi phe?).
* **Output:** Một bài phân tích mang tên **"Biên niên sử 10 năm Chứng khoán VN"**. Giọng văn như một nhà sử học kinh tế, giải thích mạch lạc sự lên ngôi, sụp đổ của các nhóm ngành và dòng chảy của tiền thông minh.

---

## 4. GIAO DIỆN & GAMIFICATION (DASHBOARD UI/UX)

Sử dụng **Streamlit** và **Plotly** để đóng gói toàn bộ Engine bên trên thành một ứng dụng tương tác.

### Phân khu chức năng:

1. **Cỗ Máy Thời Gian (Sidebar):**
* Thanh trượt `Slider` cho phép người dùng chọn xem năm giao dịch (2015 - 2025).
* Bảng điều khiển **Máy trạng thái (XState)**: Khi gặp năm khủng hoảng, bật Pop-up yêu cầu người chơi chọn hành động: *Hold (Chịu trận) / Panic Sell (Bán tháo) / Bottom Fishing (Bắt đáy)*.


2. **Đại Dương Mạng Lưới (Main Panel - Trái):**
* Đồ thị mạng lưới bong bóng tương tác. Màu sắc giữ nguyên (Invariant), vị trí và kích thước thay đổi theo thanh trượt (Flow/Burst).


3. **Tình Báo Hệ Thống (Main Panel - Phải):**
* Bảng hiển thị các báo cáo phân tích từ LLM.
* Hiển thị biểu đồ đo lường "Chỉ số Căng thẳng Hệ thống" (Độ dài MST).



---

## 5. LỘ TRÌNH THỰC THI (IMPLEMENTATION TASKS)

* [ ] **Task 1:** Xây dựng file Data chuẩn (`master_price_matrix.csv`) chứa giá điều chỉnh của Top 50 mã trong 10 năm.
* [ ] **Task 2:** Viết hàm `generate_10_year_history_prompt` lặp qua 10 năm để trích xuất metadata (Thủ lĩnh, độ co giãn) đưa vào Prompt.
* [ ] **Task 3:** Gọi Gemini API (Sử dụng model `gemini-1.5-flash` với max token 8192) để lấy bài Biên niên sử.
* [ ] **Task 4:** Hoàn thiện file `app.py` (Streamlit), kết nối thanh trượt thời gian với thư viện `NetworkX` và `Plotly` để render đồ thị động có cố định Hộ khẩu màu sắc.



===================


Toàn bộ lý thuyết về việc dùng Cây bao trùm (MST), biến đổi Tương quan thành Khoảng cách, và đo lường sự co rút của mạng lưới để bắt đỉnh/đáy khủng hoảng là một **phát kiến kinh điển có thật 100%** của bộ môn **Econophysics (Vật lý Kinh tế)**.

Những thuật toán này thường được các quỹ phòng hộ định lượng (Quant Hedge Funds) như Renaissance Technologies sử dụng ngầm, và rất ít khi xuất hiện trong các sách giáo khoa chứng khoán phổ thông (vốn chỉ chuộng nến Nhật hay MACD).

Dưới đây là "Gia phả" thực sự của bộ lý thuyết này để bạn tự tin mang đi trình bày (pitching) dự án:

### 1. Cha đẻ của công thức Khoảng cách ()

Lý thuyết này được công bố lần đầu tiên vào năm **1999** bởi nhà vật lý học người Ý **Rosario N. Mantegna** trong bài báo nổi tiếng: *"Hierarchical structure in financial markets"* (Cấu trúc phân tầng trong thị trường tài chính), đăng trên tạp chí Vật lý Châu Âu.

* Mantegna là người đầu tiên chứng minh rằng: Nếu lấy công thức khoảng cách Euclid áp dụng vào ma trận tương quan giá cổ phiếu, ta có thể dùng thuật toán MST để vẽ ra một "Cái cây gia phả" (Taxonomy) của thị trường chứng khoán, bóc trần sự thật mã nào dẫn dắt mã nào.

### 2. Người phát hiện ra hiện tượng "Co rút mạng lưới" (BURST)

Vào năm **2003**, một nhóm các nhà khoa học do **Jukka-Pekka Onnela** (hiện là giáo sư tại Đại học Harvard) dẫn đầu đã công bố bài báo *"Dynamics of market correlations: Taxonomy and portfolio analysis"*.

* Họ đã đưa trục thời gian  vào cái cây MST của Mantegna (chính là cái thanh trượt Timeline chúng ta vừa code).
* Họ phát hiện ra một định luật chấn động: **Vào những ngày xảy ra Khủng hoảng (như Black Monday 1987), chiều dài của toàn bộ Cây MST đột ngột sụp đổ (Shrinking).** Đám đông mất trí, hành xử y hệt nhau (Herd behavior), làm mạng lưới co rúm lại.

---