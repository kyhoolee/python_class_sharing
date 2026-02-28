## Target
- Module này dạy cơ bản về bài toán thu thập dữ liệu với Python 

## Detail 

### Web-crawling 
- Web là gì, Internet là gì, http protocol là gì ?
- HTML, CSS, JS là gì ?
- Bóc dữ liệu, parse dữ liệu thế nào 


## EDA cơ bản 
- Pandas là gì 
- Mathplotlib là gì 
- Từ giả định tới insight 
- Từ insight tới hành động -> bài tiếp sau -> Predicting model 


## TOOL 

Bộ 3 quyền lực: **Pandas - Matplotlib - Seaborn**.

---

## PHẦN GIỮA: GIẢI MÃ CÔNG CỤ (THE TOOLKIT DECODED) (15 Phút)

### 1. Pandas: "Excel trên Steroids" (The Brain)

Đây là trái tim của mọi dự án phân tích dữ liệu.

* **Định nghĩa trực quan:**
* Hãy tưởng tượng **Pandas** là một **File Excel siêu tốc** không có giao diện (no-GUI). Nó không cần hiện ra các ô vuông để bạn nhìn thấy, nên nó chạy cực nhanh.
* **DataFrame:** Chính là một **Worksheet** (Sheet1).
* **Series:** Chính là một **Column** (Cột A, Cột B).
* **Index:** Chính là số thứ tự dòng (1, 2, 3...) nhưng mạnh hơn vì có thể là Ngày tháng hoặc Tên mã CK.


* **Bảng từ điển (Excel to Pandas):**
* *Filter (Lọc):* `df[df['Gia'] > 10]`
* *VLOOKUP:* `pd.merge()`
* *Pivot Table:* `df.pivot_table()`
* *Remove Duplicates:* `df.drop_duplicates()`
* *Fill NA (Điền ô trống):* `df.fillna(0)`


* **Cách tự học (How to play):**
* **Keyword:** "Pandas Cheat Sheet". In tờ giấy này dán lên tường.
* **Mẹo:** Gõ `df.` rồi nhấn phím **Tab**. Nó sẽ xổ ra tất cả các "công thức" bạn có thể dùng trên bảng dữ liệu đó.



### 2. Matplotlib: "Họa sĩ hàn lâm" (The Skeleton)

Đây là thư viện vẽ hình *cơ bản nhất*, *lâu đời nhất* và *khó tính nhất*.

* **Định nghĩa trực quan:**
* Hãy tưởng tượng **Matplotlib** giống như bạn vẽ tranh bằng **Giấy trắng và Bút chì**.
* Bạn phải ra lệnh cho nó từng tí một: "Vẽ cái trục ngang", "Vẽ cái trục dọc", "Vẽ đường thẳng màu đỏ", "Viết chữ vào góc này".
* **Ưu điểm:** Bạn kiểm soát được từng pixel (muốn sửa gì cũng được).
* **Nhược điểm:** Code dài, màu mặc định trông hơi... "quê" và cũ kỹ.


* **Tại sao vẫn phải học?**
* Vì nó là "cái móng nhà". Các thư viện xịn xò khác đều xây trên nền tảng của nó. Đôi khi bạn muốn chỉnh sửa sâu vào biểu đồ, bạn phải dùng lệnh của Matplotlib.


* **Cách tự học (How to play):**
* Copy code mẫu từ trang chủ `matplotlib.org/gallery`. Đừng cố nhớ lệnh, hãy copy và sửa (Tweak).



### 3. Seaborn: "Chuyên gia trang điểm" (The Skin)

Đây là thư viện được xây dựng *trên vai* Matplotlib, dành riêng cho dân thống kê/tài chính.

* **Định nghĩa trực quan:**
* **Seaborn** giống như tính năng **Recommended Charts** hoặc **Smart Art** trong Excel 365.
* Nó thông minh: Bạn chỉ cần đưa dữ liệu vào, nó tự biết cách chọn màu đẹp, tự vẽ đường viền, tự làm mờ background cho sang trọng.
* Nó hiểu thống kê: Nó vẽ được các biểu đồ phức tạp (Heatmap, Violin plot, Regression) chỉ bằng 1 dòng code.


* **So sánh vui:**
* *Matplotlib:* Bạn đưa cây gỗ, cái cưa, cái đục -> Bạn tự đóng cái ghế.
* *Seaborn:* Bạn đưa tiền -> Nó giao cho bạn cái ghế Sofa da Ý.


* **Cách tự học (How to play):**
* **Keyword:** "Seaborn Gallery". Vào đó xem hình nào đẹp, copy code về thay dữ liệu của mình vào là xong.
* Thử đổi `palette` (bảng màu) để thấy biểu đồ đổi màu ảo diệu: `sns.set_palette("husl")`.



---

### MẸO "CHƠI" VỚI DATA (SELF-STUDY GUIDE CHO HỌC VIÊN)

1. **Quy tắc "Chấm - Tab" (.Tab)**
* Dạy họ cách khám phá. Trong Jupyter Notebook/Colab, sau khi gõ tên biến (ví dụ `df`), hãy gõ dấu chấm `.` và chờ 1 giây (hoặc nhấn Tab).
* Một danh sách gợi ý sẽ hiện ra. Thấy cái nào tên quen quen (như `mean`, `sum`, `plot`) thì chọn thử xem nó ra cái gì. Đây là cách học *thử-sai* nhanh nhất.


2. **Hỏi AI đúng cách (Pair Programming)**
* Đừng bắt họ nhớ cú pháp (Syntax). Hãy dạy họ cách hỏi ChatGPT/Gemini:
* *Prompt mẫu:* "Tôi có một dataframe tên là `df` có cột `Close` và `Date`. Hãy viết code Python dùng thư viện Seaborn để vẽ biểu đồ đường, màu xanh lá cây." -> Copy code đó dán vào chạy.


3. **Tư duy "Mảnh ghép Lego"**
* Lập trình Python cho phân tích dữ liệu không phải là viết văn (viết từ đầu đến cuối).
* Nó là xếp Lego:
* Mảnh 1: Code lấy dữ liệu (Copy từ bài học).
* Mảnh 2: Code làm sạch (Copy từ StackOverflow).
* Mảnh 3: Code vẽ hình (Copy từ Gallery).


* Nhiệm vụ là nối các mảnh đó lại (biến đầu ra của mảnh 1 là đầu vào của mảnh 2).



---

### Cập nhật cấu trúc bài giảng 1 (EDA)


1. **Thực trạng & Nỗi đau:** Crawl data khó thế nào (Request vs Selenium). -> *Học viên thấy cần giải pháp.*
2. **Giải pháp công cụ (Lý thuyết):** Giới thiệu bộ 3 (Pandas/Matplotlib/Seaborn) theo cách trực quan ở trên. -> *Học viên hiểu mình đang cầm vũ khí gì.*
3. **Thực chiến (Code):** Đi vào từng bước Crawl -> Clean -> EDA như đã soạn. -> *Học viên thấy vũ khí hoạt động.*
4. **Bài tập:** Tự tay làm.