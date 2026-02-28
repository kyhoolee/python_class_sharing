### BƯỚC 1: LỌC "VÀNG" KHỎI "CÁT" (Tạo rổ Top 50 VN-Smart)

*Dữ liệu sử dụng: `Price_History.csv` và `Financial_Ratios.csv*`

Thay vì chạy hết 1500 mã, chúng ta viết một kịch bản lọc tự động:

1. **Màng lọc Thanh khoản (Chống nhốt hàng):** Dùng `KhoiLuongKhopLenh`  `GiaDongCua` của 60 phiên gần nhất. Chỉ lấy những mã có giá trị giao dịch trung bình > 10 tỷ VNĐ/ngày.
2. **Màng lọc "Sinh tồn" (Đủ lịch sử):** Đếm số dòng (số ngày giao dịch) trong `Price_History`. Loại bỏ các mã mới lên sàn chưa đủ 3 năm (thiếu data để phân tích chu kỳ).
3. **Màng lọc Invariant (Loại rác):** Join (Kết nối) với bảng `Financial_Ratios.csv`. Loại bỏ ngay lập tức những mã có `EPS` âm hoặc `ROE` < 5% trong năm gần nhất.

*=> Kết quả: Từ 1500 mã, ta chắt lọc ra được "Top 50 - 100 mã tinh hoa". Đây là sân chơi an toàn để học viên bắt đầu.*

---

### BƯỚC 2: STORYTELLING "ĐẶC SẢN" VN-INDEX BẰNG DỮ LIỆU NGÀY

*Dữ liệu sử dụng: `Price_History.csv*`

Vì không có dữ liệu giờ/phút để soi T+2.5 hay ATC, chúng ta sẽ kể câu chuyện qua **Hình thái Nến ngày (Daily Candlestick)** và **Khoảng trống giá (Gap)**:

**1. Cú lừa thị giác của "Ngày Không Hưởng Quyền" (Dividend Drop)**

* *Story:* Người mới chơi mở bảng điện thấy cổ phiếu mình chia đôi giá (giảm 50%) thì hoảng loạn, nhưng thực chất tài sản không đổi do được nhận cổ tức.
* *Code:* Vẽ 2 đường line đè lên nhau. Đường 1 là `GiaDongCua` (sẽ thấy gãy gập vỡ nát). Đường 2 là `GiaDieuChinh` (vẫn trơn tru đi lên). Bài học: *Luôn phân tích tỷ suất sinh lời trên `GiaDieuChinh`.*

**2. Đo lường "Tâm lý qua đêm" (Overnight Gap / Hiệu ứng ATO)**

* *Story:* Sau một đêm có tin tức (bắt bớ, hoặc Dow Jones tăng mạnh), nhà đầu tư VN phản ứng thế nào lúc mở cửa?
* *Code:* So sánh `GiaMoCua` (hôm nay) với `GiaDongCua` (hôm qua). Nếu chênh lệch quá 3%, đó là một "Tâm lý bầy đàn" (Burst). Thống kê xem bao nhiêu lần Gap này bị lấp lại trong ngày (giá quay về điểm cũ).

**3. Khẩu vị rủi ro qua "Râu nến" (Shadow/Wick Analysis)**

* *Story:* Những mã đầu cơ thường bị kéo trần đầu ngày rồi đạp sàn cuối ngày, tạo ra biên độ rất lớn.
* *Code:* Tính công thức: `GiaCaoNhat` - `GiaThapNhat`. Vẽ biểu đồ phân phối. Học viên sẽ thấy rổ VN30 thì biên độ mỏng xẹt, trong khi các mã Penny thì biên độ rộng ngoác -> Cảnh báo rủi ro bạo phát bạo tàn.

---

### BƯỚC 3: DÒNG CHẢY & TÍNH TƯƠNG QUAN GIỮA CÁC ĐÀN CÁ (FLOW)

*Dữ liệu sử dụng: Cột `GiaDieuChinh` của Top 50 mã*

Bây giờ ta xếp 50 mã này cạnh nhau để tìm ra quy luật "dẫn dắt":

**1. Ma trận Tương quan (Heatmap)**

* Biến đổi `GiaDieuChinh` thành **Log-Return** (tỷ suất sinh lời hàng ngày).
* Chạy hàm `df.corr()` và vẽ Heatmap. Học viên sẽ thấy những "cục màu đậm": HPG tương quan mạnh với HSG (Cùng ngành thép), nhưng VCB (Bank) lại có lúc lệch pha với VIC (Bất động sản).

**2. Truy tìm "Con đầu đàn" (Leader Identification)**

* Dùng dữ liệu từ `cafef_api.py` để gắn nhãn Ngành (Industry) cho Top 50 mã.
* Tính tổng `KhoiLuongKhopLenh * GiaDongCua` của cả nhóm Ngành theo từng ngày.
* *Trực quan hóa:* Vẽ biểu đồ miền (Area Chart) dòng tiền của 3 nhóm lớn (Bank - Thép - BĐS). Quan sát quá khứ để thấy: *Tiền có thực sự chảy từ Bank sang Midcap rồi chốt ở Penny như lời đồn không?*

---