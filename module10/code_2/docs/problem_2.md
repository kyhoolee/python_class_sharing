# 📊 ĐỀ BÀI EDA: "NHỊP ĐẬP THỊ TRƯỜNG 10 NĂM QUA CON SỐ"

## PHẦN 1: BỨC TRANH TOÀN CẢNH (MARKET OVERVIEW)

*Mục tiêu: Hiểu "tính nết" của thị trường chứng khoán Việt Nam trong 10 năm qua.*

**Câu hỏi 1: Sự tiến hóa của quy mô (Market Cap Evolution)**

* **Ý nghĩa:** Dòng tiền vào thị trường đã lớn lên như thế nào?
* **Data Question:** Tính tổng Vốn hóa (MarketCap) và Tổng Thanh khoản (Volume) của toàn thị trường theo từng năm.
* **Chart:** Biểu đồ kết hợp (Combo Chart): Bar (Volume) và Line (MarketCap).
* **Insight tìm kiếm:** Năm nào dòng tiền bùng nổ nhất? Có phải khi MarketCap đạt đỉnh thì Volume cũng đạt đỉnh không?

**Câu hỏi 2: Thị trường "dữ dằn" cỡ nào? (Volatility Check)**

* **Ý nghĩa:** Đo lường rủi ro tổng thể.
* **Data Question:** Tính số phiên tăng/giảm > 2% của VN-Index (hoặc đại diện là trung bình các mã Bluechip) trong từng năm.
* **Chart:** Bar chart tần suất các phiên biến động mạnh.
* **Insight tìm kiếm:** Năm nào thị trường "yên bình" nhất? Năm nào "xóc" nhất?

---

## PHẦN 2: PHÂN TÍCH THEO GIAI ĐOẠN (PERIOD ANALYSIS)

*Mục tiêu: So sánh hành vi thị trường qua các thời kỳ kinh tế khác nhau.*

**Giai đoạn A: Tích lũy & Tăng trưởng (2015 - 2020)**

* **Bối cảnh:** Kinh tế vĩ mô ổn định, chưa có Covid.
* **Câu hỏi:** Nhóm ngành nào mang lại lợi nhuận bền vững nhất (Consistent Growth) trong giai đoạn này? (Gợi ý: So sánh CAGR của Ngân hàng vs. Sản xuất).

**Giai đoạn B: Kỷ nguyên tiền rẻ (2020 - 2022)**

* **Bối cảnh:** Covid, lãi suất thấp, F0 đổ vào chứng khoán.
* **Câu hỏi:**
* "Thuyền lên nước lên": Có bao nhiêu % cổ phiếu tăng gấp đôi (x2) trong giai đoạn này?
* Sự trỗi dậy của Penny: So sánh mức tăng giá trung bình của nhóm vốn hóa nhỏ (SmallCap) so với VN30. Có phải "rác cũng thành vàng"?



**Giai đoạn C: Cú sập & Bình thường mới (2022 - 2025)**

* **Bối cảnh:** Bắt bớ, trái phiếu, lãi suất tăng, phục hồi.
* **Câu hỏi:**
* Ai là "kẻ sống sót"? Lọc ra những mã cổ phiếu đã vượt đỉnh cũ của năm 2022 hoặc giảm ít nhất trong cú sập.
* Định giá (P/E) đã về mức rẻ chưa? So sánh P/E trung bình năm 2024 so với đỉnh 2021.



---

## PHẦN 3: PHÂN TÍCH NHÓM NGÀNH (SECTOR ANALYSIS)

*Mục tiêu: Tìm ra "Long mạch" của dòng tiền.*

**Câu hỏi 3: Đặc tính ngành (Sector Personality)**

* **Ngành nào "nhạy" nhất (High Beta)?** Khi thị trường tăng 1%, ngành nào thường tăng mạnh hơn (Chứng khoán, Bất động sản)?
* **Ngành nào "phòng thủ" nhất (Low Beta)?** Khi thị trường sập, ngành nào giữ giá tốt nhất (Điện, Nước, Y tế)?
* **Tech Hint:** Tính Correlation Matrix giữa Index ngành và Index thị trường.

**Câu hỏi 4: Chu kỳ lợi nhuận (Profit Cycle)**

* **Ý nghĩa:** Ngành nào có lợi nhuận theo mùa vụ hoặc chu kỳ kinh tế?
* **Data Question:** Vẽ biểu đồ tăng trưởng lợi nhuận ròng (Net Profit Growth) theo quý của ngành Thép (chu kỳ hàng hóa) vs. ngành Công nghệ (tăng trưởng bền vững).

---

## PHẦN 4: CỔ PHIẾU NỔI BẬT (STOCK PICKING)

*Mục tiêu: Đãi cát tìm vàng.*

**Câu hỏi 5: Tìm kiếm "Siêu cổ phiếu" (Super Stocks)**

* Hãy tìm ra Top 5 cổ phiếu thỏa mãn tiêu chí "CANSLIM" đơn giản hóa:
* Doanh thu tăng trưởng dương 3 năm liên tiếp.
* Lợi nhuận tăng trưởng dương 3 năm liên tiếp.
* Giá hiện tại > MA200 (đang trong xu hướng tăng dài hạn).



**Câu hỏi 6: Cổ phiếu "lạ" (Anomalies)**

* Tìm những mã có Volume cực thấp (thanh khoản kém) nhưng giá tăng liên tục (cổ phiếu cô đặc/bị thâu tóm).
* Tìm những mã có Lợi nhuận rất cao nhưng P/E lẹt đẹt mãi không tăng (Bẫy giá trị - Value Trap).

---

## PHẦN 5: KIỂM ĐỊNH XU HƯỚNG (TREND STABILITY)

*Mục tiêu: Phân biệt đâu là quy luật, đâu là ngẫu nhiên.*

**Câu hỏi 7: Xu hướng ổn định (Immutable Trends)**

* *Giả thuyết:* "Tháng 5 và Tháng 11 luôn là tháng xấu/tốt?" (Sell in May?).
* *Action:* Tính lợi nhuận trung bình theo tháng (Month Seasonality) trong suốt 10 năm. Có tháng nào luôn xanh hoặc luôn đỏ không?

**Câu hỏi 8: Xu hướng đã thay đổi (Broken Trends)**

* *Quan hệ P/E và Lãi suất:* Trước 2020, lãi suất giảm thì P/E tăng. Từ 2022-2025, mối quan hệ này còn đúng không hay đã bị phá vỡ bởi các yếu tố khác (tỷ giá, trái phiếu)?
* *Thanh khoản và Giá:* Ngày xưa (2015-2018), Volume đột biến thường là đỉnh ngắn hạn. Trong giai đoạn 2020-2022, Volume đột biến lại là khởi đầu sóng tăng. Hãy vẽ Scatter plot để kiểm chứng.

---

### GỢI Ý KỸ THUẬT (Dành cho học viên)

Để giải quyết các câu hỏi trên, học viên sẽ cần vận dụng:

1. **Pandas Resample/Grouper:** Để gom dữ liệu từ Ngày sang Tháng/Quý/Năm.
* *Code:* `df.set_index('Ngay').resample('Y').sum()`


2. **Window Functions:** Để tính % thay đổi giá, MA, Rolling Volatility.
* *Code:* `df['Close'].pct_change()`, `df['Close'].rolling(20).std()`


3. **Merge/Join:** Để ghép bảng Giá (Price) với bảng Tài chính (Finance) nhằm tính P/E.
4. **Seaborn Heatmap:** Để vẽ ma trận tương quan giữa các ngành.
5. **Matplotlib Subplots:** Để vẽ so sánh 3 giai đoạn (2015-2020, 2020-2022, 2022-2025) cạnh nhau.

