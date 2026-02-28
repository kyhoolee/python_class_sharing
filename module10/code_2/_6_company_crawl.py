import pandas as pd
import requests
import time
import os

print("[*] KHỞI ĐỘNG MODULE THU THẬP HỒ SƠ DOANH NGHIỆP...")

# 1. LẤY DANH SÁCH MÃ CỔ PHIẾU TỪ DATABASE ĐÃ CÓ
# Chúng ta đọc bảng Micro để lấy chính xác các mã đang nằm trong mạng lưới
try:
    df_micro = pd.read_csv("db_micro_nodes.csv")
    symbols = sorted(df_micro['Symbol'].unique())
    print(f"[+] Tìm thấy {len(symbols)} mã cổ phiếu cần thu thập hồ sơ.")
except FileNotFoundError:
    print("[!] Không tìm thấy file db_micro_nodes.csv. Vui lòng chạy file bóc tách Network trước!")
    exit()

# 2. CẤU HÌNH CRAWLER
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://cafef.vn/"
}

profiles = []

# 3. CHẠY VÒNG LẶP GỌI API CAFEF
print("\n[*] BẮT ĐẦU CRAWL (Sẽ mất khoảng vài chục giây để tránh bị block IP)...")

for i, sym in enumerate(symbols):
    url = f"https://cafef.vn/du-lieu/Ajax/PageNew/CompanyIntro.ashx?Symbol={sym}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        # Kiểm tra HTTP Status
        if response.status_code == 200:
            res_json = response.json()
            
            # Bóc tách Data theo chuẩn cấu trúc JSON của CafeF
            if res_json.get("Success") and res_json.get("Data"):
                data = res_json["Data"]
                
                company_name = data.get("Name", sym)
                intro = data.get("Intro", "")
                website = data.get("Web", "")
                
                profiles.append({
                    "Symbol": sym,
                    "Company_Name": company_name,
                    "Description": intro,
                    "Website": website
                })
                print(f"  [{i+1}/{len(symbols)}] Tải thành công: {sym} - {company_name}")
            else:
                print(f"  [{i+1}/{len(symbols)}] [!] Dữ liệu API rỗng cho mã: {sym}")
                profiles.append({"Symbol": sym, "Company_Name": sym, "Description": "Không có dữ liệu", "Website": ""})
        else:
            print(f"  [{i+1}/{len(symbols)}] [!] Lỗi kết nối HTTP {response.status_code} tại {sym}")
            profiles.append({"Symbol": sym, "Company_Name": sym, "Description": "Lỗi kết nối", "Website": ""})
            
    except Exception as e:
        print(f"  [{i+1}/{len(symbols)}] [x] Lỗi Exception tại {sym}: {e}")
        profiles.append({"Symbol": sym, "Company_Name": sym, "Description": f"Lỗi hệ thống", "Website": ""})
    
    # Dừng 0.5s giữa mỗi request để tôn trọng server CafeF (Polite Crawling)
    time.sleep(0.5)

# 4. LƯU THÀNH FILE DATABASE THỨ 4
df_profiles = pd.DataFrame(profiles)

# Làm sạch text (Xóa các ký tự \r, \n dư thừa trong chuỗi mô tả)
df_profiles['Description'] = df_profiles['Description'].replace(r'\r+|\n+|\t+', ' ', regex=True)

df_profiles.to_csv("db_company_profiles.csv", index=False)

print("\n[+] HOÀN TẤT! Đã lưu hồ sơ doanh nghiệp vào file 'db_company_profiles.csv'.")
print(df_profiles.head())