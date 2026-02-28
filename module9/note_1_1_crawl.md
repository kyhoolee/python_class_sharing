# CẤU TRÚC SLIDE: PYTHON FOR FINANCE - DATA CRAWLING MASTERCLASS

**Thời lượng:** 120 phút
**Đối tượng:** Chuyên viên Tài chính / Kế toán / Phân tích dữ liệu

---

## PHẦN 1: TƯ DUY & CÔNG CỤ (MINDSET)

### Slide 1: Title Slide

* **Tiêu đề:** TỰ ĐỘNG HÓA THU THẬP DỮ LIỆU TÀI CHÍNH (DATA CRAWLING)
* **Phụ đề:** Biến Python thành trợ lý đắc lực thay thế Copy-Paste thủ công
* **Người trình bày:** [Tên bạn]
* **Hình ảnh minh họa:**

### Slide 2: Vấn đề & Giải pháp

* **Nỗi đau (Pain Points):**
* Mở 10 tab web để copy giá mỗi sáng.
* Dữ liệu bị lệch dòng khi paste vào Excel.
* Không thể cập nhật realtime khi thị trường biến động.


* **Giải pháp Python:**
* **Tốc độ:** Xử lý 100 mã trong 30 giây.
* **Chính xác:** Máy tính không biết mỏi, không copy nhầm dòng.
* **Tự động:** Hẹn giờ chạy báo cáo trước khi bạn ngủ dậy.



### Slide 3: Giải phẫu một trang web (Web Anatomy)

* **Trình duyệt (Browser):** Giống như cái **Máy in**. Nó nhận code và "in" ra giao diện đẹp cho mắt người xem.
* **Source Code (HTML):** Giống như **Bộ xương**. Chứa dữ liệu thô mà chúng ta cần lấy.
* **Inspect Element (F12):**
* Là "Máy chụp X-Quang" của Data Analyst.
* Giúp nhìn xuyên qua giao diện để thấy dữ liệu gốc nằm ở đâu.


* *[Hình ảnh minh họa: Screenshot so sánh giao diện CafeF và màn hình F12 đầy code]*

### Slide 4: Chiến thuật: Biến số & Hằng số

* **Quy luật của Crawling:** Tìm ra những thứ lặp lại.
* **Hằng số (Cố định):**
* Tên miền: `cafef.vn`
* Cấu trúc bảng: `<table class="report">`


* **Biến số (Thay đổi):**
* Mã cổ phiếu: `HPG`, `VIC`, `VNM`
* Số trang: `page=1`, `page=2`


* **Ví dụ URL:** `https://cafef.vn/du-lieu/{BIẾN_SỐ}.chn`

---

## PHẦN 2: THỰC HÀNH CRAWL (LEVEL 1 & 2)

### Slide 5: Level 1 - "Con đường bí mật" (Hidden API)

* **Phương pháp:** Tìm API JSON ẩn sau giao diện web.
* **Đặc điểm:** Nhanh, sạch, dữ liệu dạng Key-Value.
* **Công cụ:** `Network Tab` (trong F12) + Thư viện `requests`.
* **Ví dụ:** Lấy lịch sử giá CafeF.
* URL không phải là `.html` mà là `.ashx` hoặc `.json`.
* Kết quả trả về sạch sẽ, không cần lọc thẻ HTML.



### Slide 6: Demo Code - Lấy dữ liệu API

*(Chèn đoạn code Python gọn gàng)*

```python
import requests
import pandas as pd

url = "https://cafef.vn/.../PriceHistory.ashx"
params = {"Symbol": "HPG"}
data = requests.get(url, params=params).json()

# Chuyển ngay thành Excel
df = pd.DataFrame(data['Data']['Data'])

```

* **Note:** Chỉ cần thay `Symbol` là lấy được mã khác.

### Slide 7: Level 2 - Quét Web Tĩnh (Static HTML)

* **Đối tượng:** Các trang web công nghệ cũ (Cophieu68, Vietstock cũ).
* **Đặc điểm:** Server gửi về là có sẵn dữ liệu trong bảng.
* **Vũ khí tối thượng:** `pandas.read_html(url)`
* **Sức mạnh:** Tự động tìm thẻ `<table>` và chuyển thành Excel trong 1 dòng code.

---

## PHẦN 3: THỰC HÀNH NÂNG CAO (LEVEL 3 - SELENIUM)

### Slide 8: Thách thức - Web Động & Bảo Mật

* **Vấn đề 1 (Loading):** Web hiện đại (React/Vue) tải cái khung trước, dữ liệu tải sau 3-5 giây.
* -> `Requests` chỉ lấy được cái khung rỗng.


* **Vấn đề 2 (Anti-Bot):** Web chặn các truy cập không phải người thật.
* **Vấn đề 3 (Redirect):** Tự động chuyển hướng từ Mobile sang Desktop.

### Slide 9: Giải pháp - Selenium (Robot giả lập)

* **Cơ chế:**
1. Mở trình duyệt Chrome thật (do code điều khiển).
2. Truy cập trang web.
3. **QUAN TRỌNG:** Ngồi đợi (`Wait`) cho dữ liệu tải xong.
4. Lấy HTML về để xử lý.


* *[Hình ảnh minh họa: Icon con Robot đang điều khiển logo Chrome]*

### Slide 10: Kỹ thuật "Tàng hình" (Stealth Mode)

* Để không bị chặn, Robot phải giả làm người:
* **Fake User-Agent:** "Tôi là Windows 10, Chrome xịn".
* **Disable Automation Flags:** Xóa dòng chữ "Chrome is controlled by automated software".


* **Code Snippet:**

```python
options.add_argument("user-agent=Mozilla/5.0...")
options.add_argument("--disable-blink-features=AutomationControlled")

```

### Slide 11: Kỹ thuật "Phẫu thuật" (Parsing Strategies)

* Làm sao lấy dữ liệu khi tên Class thay đổi liên tục?
* **Chiến thuật 1: Tìm theo ID/Class cố định.** (Dùng cho web cấu trúc rõ ràng).
* **Chiến thuật 2: Keyword Search (Tìm theo từ khóa).**
* "Tìm cho tôi chữ **EPS**, rồi lấy con số nằm ngay bên cạnh nó".
* Bền vững hơn, ít lỗi khi web update giao diện.



### Slide 12: Case Study thực tế - CafeF Desktop

* **Tình huống:** Bị redirect từ Mobile -> Desktop.
* **Xử lý:**
* Chấp nhận crawl trên giao diện Desktop.
* Dùng `BeautifulSoup` để lọc các ô rỗng trong bảng Tài chính.
* Kết hợp `find(string="P/E")` để lấy chỉ số định giá.



---

## PHẦN 4: TỔNG KẾT

### Slide 13: Quy trình chuẩn của Data Engineer

1. **Điều tra (Investigate):** Web Tĩnh hay Động? Có API không? (Dùng F12).
2. **Chiến thuật (Strategy):** Chọn `Requests` (nếu dễ) hoặc `Selenium` (nếu khó).
3. **Code & Debug:** Xử lý anti-bot, chờ loading.
4. **Parsing:** Làm sạch dữ liệu, lưu file Excel.

### Slide 14: Q&A và Bài tập về nhà

* **Bài tập:** Xây dựng Bot cập nhật danh mục đầu tư cá nhân mỗi sáng (Giá, P/E, EPS) từ danh sách mã tùy chọn.
* **Tài nguyên:** Link Github code mẫu, Cheat Sheet các hàm Pandas.

---

