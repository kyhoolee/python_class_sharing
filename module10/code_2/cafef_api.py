import os
import time
import requests
import pandas as pd
from datetime import datetime
import logging

# ==============================================================================
# CẤU HÌNH HỆ THỐNG
# ==============================================================================
DATA_FOLDER = "Data_Cube"       # Tên thư mục gốc chứa dữ liệu
DELAY_BETWEEN_STOCKS = 1.5      # Giây nghỉ giữa các mã (để tránh bị chặn IP)
DELAY_BETWEEN_APIS = 0.5        # Giây nghỉ giữa các API trong cùng 1 mã

# Header giả lập trình duyệt (Rất quan trọng)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://cafef.vn/"
}

# Danh sách ID ngành (CafeF)
SECTOR_MAP = {
    345: "BatDongSan_XayDung",
    347: "CongNghe",
    343: "CongNghiep",
    346: "DichVu",
    339: "HangTieuDung",
    340: "NangLuong",
    344: "NguyenVatLieu",
    338: "NongNghiep",
    341: "TaiChinh",
    348: "VienThong",
    342: "YTe"
}

# Danh sách sàn giao dịch (1: HOSE, 2: HNX, 9: UPCOM)
# Bạn có thể bỏ bớt nếu chỉ muốn lấy HOSE
CENTER_IDS = [1, 2, 9] 

# ==============================================================================
# MODULE: LOGGER (GHI LOG CHI TIẾT)
# ==============================================================================
def log(message, level="INFO"):
    """Hàm in log ra màn hình có kèm thời gian"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

# ==============================================================================
# MODULE: API FETCHERS (LẤY DỮ LIỆU)
# ==============================================================================

def get_market_stock_list():
    """Lấy danh sách toàn bộ mã theo ngành và sàn"""
    master_list = []
    log("Bắt đầu quét danh sách mã chứng khoán toàn thị trường...", "START")
    
    for center_id in CENTER_IDS:
        center_name = {1: "HOSE", 2: "HNX", 9: "UPCOM"}.get(center_id, "Unknown")
        
        for sector_id, sector_name in SECTOR_MAP.items():
            url = "https://cafef.vn/du-lieu/ajax/mobile/smart/ajaxbandothitruong.ashx"
            params = {"type": 1, "category": sector_id, "centerId": center_id}
            
            try:
                r = requests.get(url, params=params, headers=HEADERS, timeout=10)
                data = r.json()
                
                if 'Data' in data and data['Data']:
                    count = len(data['Data'])
                    log(f"Quét {center_name} - {sector_name}: Tìm thấy {count} mã.")
                    
                    for item in data['Data']:
                        master_list.append({
                            'Symbol': item['Symbol'],
                            'Industry': sector_name,
                            'Exchange': center_name,
                            'MarketCap': item.get('MarketCap', 0)
                        })
                time.sleep(0.2) # Nghỉ nhẹ
            except Exception as e:
                log(f"Lỗi quét ngành {sector_name} sàn {center_name}: {e}", "ERROR")
                
    df = pd.DataFrame(master_list)
    # Loại bỏ mã trùng (nếu có)
    df = df.drop_duplicates(subset=['Symbol'])
    log(f"-> Tổng cộng đã tìm thấy: {len(df)} mã cổ phiếu.", "SUCCESS")
    return df

def get_price_history(symbol):
    """Lấy toàn bộ lịch sử giá"""
    url = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx"
    # PageSize 10000 đảm bảo lấy hết ~30 năm dữ liệu
    params = {"Symbol": symbol, "PageIndex": 1, "PageSize": 10000}
    
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        raw_data = r.json()['Data']['Data']
        if not raw_data: return pd.DataFrame()
        
        df = pd.DataFrame(raw_data)
        
        # Data Cleaning
        df['Ngay'] = pd.to_datetime(df['Ngay'], format='%d/%m/%Y')
        # Xóa dấu phẩy trong số (vd: 1,200 -> 1200)
        cols_num = ['GiaDieuChinh', 'GiaDongCua', 'KhoiLuongKhopLenh', 'GiaTriKhopLenh', 'GiaMoCua', 'GiaCaoNhat', 'GiaThapNhat']
        for col in cols_num:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '').astype(float)
                
        # Sắp xếp cũ -> mới
        df = df.sort_values('Ngay').reset_index(drop=True)
        return df
    except Exception as e:
        log(f"Lỗi lấy giá {symbol}: {e}", "WARN")
        return pd.DataFrame()

def get_finance_report(symbol, report_type):
    """Lấy BCTC (report_type: 'QUY' hoặc 'NAM')"""
    url = "https://cafef.vn/du-lieu/Ajax/PageNew/FinanceReport.ashx"
    
    # FIX LỖI API QUÝ: Phải truyền EndDate dạng '12-YYYY'
    # Lấy năm hiện tại + 1 để chắc chắn lấy hết dữ liệu mới nhất
    future_year = datetime.now().year + 1
    end_date = f"12-{future_year}" if report_type == 'QUY' else f"{future_year}"
    
    params = {
        "Symbol": symbol,
        "Type": 1, # 1: KQKD, 2: CĐKT. Ở đây lấy KQKD trước
        "ReportType": report_type,
        "TotalRow": 200, # Lấy 200 kỳ (50 năm) -> Vét cạn
        "EndDate": end_date
    }
    
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = r.json()
        
        if 'Data' not in data or data['Data'] is None:
            return pd.DataFrame()
            
        values = data['Data']['Value']
        processed = []
        
        for p in values:
            row = {
                'Nam': p['Year'],
                'Ky': p.get('Quater', 0),
                'LoaiBC': report_type
            }
            for item in p['Value']:
                row[item['Code']] = item['Value']
            processed.append(row)
            
        return pd.DataFrame(processed)
    except Exception as e:
        # log(f"Lỗi lấy BCTC {report_type} {symbol}: {e}", "WARN")
        return pd.DataFrame()

def get_ratios(symbol):
    """Lấy chỉ số tài chính (PE, EPS, ROE...)"""
    url = "https://cafef.vn/du-lieu/Ajax/PageNew/GetDataChiSoTaiChinh.ashx"
    params = {
        "Symbol": symbol,
        "TotalRow": 200,
        "EndDate": f"{datetime.now().year + 1}"
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = r.json()
        if 'Data' not in data or data['Data'] is None: return pd.DataFrame()
        
        values = data['Data']['Value']
        processed = []
        for p in values:
            row = {'Nam': p['Year'], 'Ky': p.get('Quater', 0)}
            for item in p['Value']:
                row[item['Code']] = item['Value']
            processed.append(row)
        return pd.DataFrame(processed)
    except:
        return pd.DataFrame()

# ==============================================================================
# MODULE: CORE ENGINE (XỬ LÝ CHÍNH)
# ==============================================================================

def process_single_stock(symbol, industry):
    """Xử lý download toàn bộ cho 1 mã"""
    
    # 1. Tạo thư mục
    # Đường dẫn: Data_Cube/TenNganh/MaCK/
    save_dir = os.path.join(DATA_FOLDER, industry, symbol)
    os.makedirs(save_dir, exist_ok=True)
    
    log(f"--- Đang xử lý: {symbol} ({industry}) ---")
    
    # 2. Download Giá
    df_price = get_price_history(symbol)
    if not df_price.empty:
        df_price.to_csv(f"{save_dir}/Price_History.csv", index=False)
        log(f"   + Giá: {len(df_price)} phiên (Từ {df_price['Ngay'].min().date()} đến {df_price['Ngay'].max().date()})")
    else:
        log(f"   ! Giá: Không có dữ liệu", "WARN")
    
    time.sleep(DELAY_BETWEEN_APIS)

    # 3. Download BCTC Quý
    df_fin_q = get_finance_report(symbol, 'QUY')
    if not df_fin_q.empty:
        df_fin_q.to_csv(f"{save_dir}/Finance_Quarter.csv", index=False)
        log(f"   + BCTC Quý: {len(df_fin_q)} bản ghi")
    
    time.sleep(DELAY_BETWEEN_APIS)
    
    # 4. Download BCTC Năm
    df_fin_y = get_finance_report(symbol, 'NAM')
    if not df_fin_y.empty:
        df_fin_y.to_csv(f"{save_dir}/Finance_Year.csv", index=False)
        log(f"   + BCTC Năm: {len(df_fin_y)} bản ghi")
        
    time.sleep(DELAY_BETWEEN_APIS)

    # 5. Download Ratios
    df_ratios = get_ratios(symbol)
    if not df_ratios.empty:
        df_ratios.to_csv(f"{save_dir}/Financial_Ratios.csv", index=False)
        log(f"   + Chỉ số: {len(df_ratios)} bản ghi")
        
    return True

# ==============================================================================
# MAIN PROGRAM
# ==============================================================================
if __name__ == "__main__":
    
    # Tạo thư mục gốc
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
        
    log("=== CHƯƠNG TRÌNH CRAWL DATA CAFEF ===", "INIT")
    
    # BƯỚC 1: LẤY DANH SÁCH MÃ
    df_tickers = get_market_stock_list()
    
    if df_tickers.empty:
        log("Không lấy được danh sách mã. Dừng chương trình.", "ERROR")
        exit()
        
    # Lưu danh sách mã ra file để tham khảo
    df_tickers.to_csv(f"{DATA_FOLDER}/_Master_Ticker_List.csv", index=False)
    
    # Lọc bỏ các mã không có vốn hóa (thường là rác hoặc hủy niêm yết) để tiết kiệm thời gian
    # df_run = df_tickers[df_tickers['MarketCap'] > 0]
    df_run = df_tickers # Hoặc chạy hết nếu muốn
    
    total_stocks = len(df_run)
    log(f"Chuẩn bị download dữ liệu cho {total_stocks} mã...", "READY")
    
    # BƯỚC 2: CHẠY VÒNG LẶP
    start_time = time.time()
    
    for i, row in df_run.iterrows():
        symbol = row['Symbol']
        industry = row['Industry']
        
        progress = f"[{i+1}/{total_stocks}]"
        print(f"\n{progress}", end=" ")
        
        try:
            process_single_stock(symbol, industry)
        except KeyboardInterrupt:
            log("Người dùng dừng chương trình!", "STOP")
            break
        except Exception as e:
            log(f"Lỗi không xác định tại {symbol}: {e}", "ERROR")
            
        # Nghỉ giữa các mã để tránh bị chặn IP
        time.sleep(DELAY_BETWEEN_STOCKS)
        
    end_time = time.time()
    duration = (end_time - start_time) / 60
    
    log("="*40)
    log(f"HOÀN TẤT! Tổng thời gian: {duration:.2f} phút.", "SUCCESS")
    log(f"Dữ liệu được lưu tại thư mục: ./{DATA_FOLDER}")