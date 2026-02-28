# BÀI TẬP THỰC HÀNH: PHÂN TÍCH DỮ LIỆU CHỨNG KHOÁN VIỆT NAM (EDA)

**Mục tiêu:**
Sử dụng Python (Pandas, Matplotlib) để đọc, xử lý và trực quan hóa dữ liệu chứng khoán thực tế đã được crawl từ CafeF.

**Cấu trúc dữ liệu:**
Giả sử dữ liệu nằm trong thư mục `Data_Cube` với cấu trúc:

```text
Data_Cube/
├── CongNghe/
│   ├── FPT/
│   │   ├── Price_History.csv
│   │   ├── Financial_Ratios.csv
│   │   └── ...
├── BatDongSan_XayDung/
│   ├── VIC/
│   └── ...

```

---

## PHẦN 1: KHỞI TẠO VÀ LOAD DỮ LIỆU

**Yêu cầu:** Import thư viện và viết hàm đọc file lịch sử giá của một mã bất kỳ.

### Gợi ý Code mẫu:

```python
import pandas as pd
import matplotlib.pyplot as plt
import os

# Cấu hình hiển thị
pd.set_option('display.max_columns', None)
plt.style.use('seaborn-v0_8') # Hoặc 'ggplot'

def load_stock_price(industry, symbol):
    """
    Hàm đọc file giá của 1 mã chứng khoán.
    Lưu ý: Thay đổi đường dẫn 'Data_Cube' nếu bạn lưu ở chỗ khác.
    """
    path = f"Data_Cube/{industry}/{symbol}/Price_History.csv"
    
    if not os.path.exists(path):
        print(f"Không tìm thấy file: {path}")
        return None
    
    # Đọc CSV
    df = pd.read_csv(path)
    
    # Chuẩn hóa cột ngày tháng
    df['Ngay'] = pd.to_datetime(df['Ngay'])
    
    # Sắp xếp theo thời gian tăng dần
    df = df.sort_values('Ngay').reset_index(drop=True)
    
    return df

# Test thử với mã FPT
df_fpt = load_stock_price("CongNghe", "FPT")

if df_fpt is not None:
    print(f"Đã load FPT: {len(df_fpt)} dòng.")
    print(df_fpt.head())

```

**🚀 Mở rộng (Challenge):**

* Hãy viết thêm code kiểm tra xem dữ liệu có bị `NaN` (trống) không?
* Tạo thêm cột `Year` và `Month` từ cột `Ngay` để tiện group dữ liệu sau này.

---

## PHẦN 2: TRỰC QUAN HÓA XU HƯỚNG GIÁ (VISUALIZATION)

**Yêu cầu:** Vẽ biểu đồ đường (Line Chart) thể hiện giá đóng cửa (`GiaDongCua`) của cổ phiếu qua các năm.

### Gợi ý Code mẫu:

```python
# Tiếp tục với df_fpt ở trên
plt.figure(figsize=(12, 6))

# Vẽ đường giá
plt.plot(df_fpt['Ngay'], df_fpt['GiaDongCua'], label='Giá Đóng Cửa', color='blue', linewidth=1.5)

# Trang trí biểu đồ
plt.title('Biểu đồ giá cổ phiếu FPT', fontsize=16)
plt.xlabel('Năm')
plt.ylabel('Giá (VND)')
plt.legend()
plt.grid(True)
plt.show()

```

**🚀 Mở rộng (Challenge):**

* **Vẽ Moving Average (MA):** Tính và vẽ thêm đường trung bình động 50 ngày (MA50) lên cùng biểu đồ để xem xu hướng dài hạn.
* *Gợi ý:* `df['MA50'] = df['GiaDongCua'].rolling(window=50).mean()`


* **Vẽ Volume:** Vẽ thêm biểu đồ cột (Bar chart) cho `KhoiLuongKhopLenh` ở bên dưới biểu đồ giá (dùng `plt.subplots`).

---

## PHẦN 3: PHÂN TÍCH BIẾN ĐỘNG (VOLATILITY & RETURN)

**Yêu cầu:** Tính lợi nhuận hàng ngày (Daily Return) và xem phân phối biến động giá.
Công thức: `Daily Return = (Giá hôm nay - Giá hôm qua) / Giá hôm qua`

### Gợi ý Code mẫu:

```python
# Tính % thay đổi giá hàng ngày
df_fpt['Return'] = df_fpt['GiaDongCua'].pct_change()

# Vẽ Histogram để xem phân phối lợi nhuận
plt.figure(figsize=(10, 5))
df_fpt['Return'].hist(bins=50, color='green', alpha=0.7)
plt.title('Phân phối lợi nhuận ngày của FPT')
plt.xlabel('Mức thay đổi (%)')
plt.ylabel('Tần suất')
plt.show()

# In ra ngày giảm mạnh nhất và tăng mạnh nhất
worst_day = df_fpt.loc[df_fpt['Return'].idxmin()]
best_day = df_fpt.loc[df_fpt['Return'].idxmax()]

print(f"Ngày giảm mạnh nhất: {worst_day['Ngay'].date()} ({worst_day['Return']:.2%})")
print(f"Ngày tăng mạnh nhất: {best_day['Ngay'].date()} ({best_day['Return']:.2%})")

```

**🚀 Mở rộng (Challenge):**

* Lọc ra các ngày mà giá biến động bất thường (Outliers): Ví dụ tăng/giảm quá 6.5% (gần trần/sàn).
* Tính độ lệch chuẩn (`std`) của cột `Return` để đo lường rủi ro.

---

## PHẦN 4: SO SÁNH TƯƠNG QUAN (CORRELATION)

**Yêu cầu:** So sánh giá của 2 cổ phiếu cùng ngành (Ví dụ: Ngành Thép - HPG và HSG) xem chúng có cùng xu hướng không.

### Gợi ý Code mẫu:

```python
# Load 2 mã (Giả sử bạn đã crawl đủ dữ liệu)
# Lưu ý: Cần đảm bảo file tồn tại trong thư mục tương ứng
df_hpg = load_stock_price("NguyenVatLieu", "HPG")
df_hsg = load_stock_price("NguyenVatLieu", "HSG")

if df_hpg is not None and df_hsg is not None:
    # Merge 2 dataframe theo ngày để so sánh cùng mốc thời gian
    df_compare = pd.merge(df_hpg[['Ngay', 'GiaDongCua']], 
                          df_hsg[['Ngay', 'GiaDongCua']], 
                          on='Ngay', suffixes=('_HPG', '_HSG'))
    
    # Tính ma trận tương quan
    corr = df_compare[['GiaDongCua_HPG', 'GiaDongCua_HSG']].corr()
    print("Ma trận tương quan:")
    print(corr)

    # Vẽ Scatter Plot
    plt.figure(figsize=(8, 8))
    plt.scatter(df_compare['GiaDongCua_HPG'], df_compare['GiaDongCua_HSG'], alpha=0.5)
    plt.title(f"Tương quan giá HPG vs HSG (Corr: {corr.iloc[0,1]:.2f})")
    plt.xlabel('Giá HPG')
    plt.ylabel('Giá HSG')
    plt.show()

```

**🚀 Mở rộng (Challenge):**

* Thay vì so sánh giá tuyệt đối, hãy so sánh `Return` (lợi nhuận ngày) của 2 mã. Điều này phản ánh chính xác hơn mức độ tương đồng về biến động.
* Thử so sánh 1 mã Ngân hàng (VCB) với 1 mã Bất động sản (VIC) xem tương quan cao hay thấp?

---

## PHẦN 5: MINI-PROJECT (TỔNG HỢP)

**Đề bài:**
Viết một chương trình nhỏ quét qua danh mục 5 mã cổ phiếu bất kỳ mà bạn có, sau đó:

1. Tính tổng lợi nhuận (Total Return) của từng mã trong năm 2023.
2. Vẽ biểu đồ cột so sánh hiệu suất của 5 mã này.

**Gợi ý logic:**

1. Tạo list: `portfolio = [("CongNghe", "FPT"), ("TaiChinh", "VCB"), ...]`
2. Dùng vòng lặp `for` để load từng mã.
3. Filter dữ liệu năm 2023 (`df['Ngay'].dt.year == 2023`).
4. Công thức Total Return: `(Giá cuối năm - Giá đầu năm) / Giá đầu năm`.
5. Lưu kết quả vào list rồi vẽ bar chart.

---