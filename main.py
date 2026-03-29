import os
import sys
import base64
from rsudblora import riwayat_pemeriksaan as blora_riwayat
from rsudblora import reservasi_dokter as blora_reservasi

def _decode(data):
    return base64.b64decode(data).decode('utf-8')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"\033[92m") # Warna Hijau
    print(r"""
    __________.__                         ___ ___         __   
    \______   \  |   ____________________/   |   \_____ _/  |_ 
     |    |  _/  |  /  _ \_  __ \__  \  \_   |   /\__  \\   __\
     |    |   \  |_(  <_> )  | \// __ \_ |   |   /  / __ \|  |  
     |______  /____/\____/|__|  (____  / |___|  /  (____  /__|  
            \/                       \/       \/         \/      
    ============================================================
    [+] Project: BloraHat Security Audit Tool
    [+] Author : Open Source Contributor
    ============================================================
    \033[0m""")

def main_menu():
    while True:
        clear()
        banner()
        print(" [1] Auth Test (Login Bypass & Token Check)")
        print(" [2] RM Scanner (Cari No RM Tersedia)")
        print(" [3] Data Extractor (Scraping)")
        print(" [0] Exit")
        print("\n")
        
        choice = input(" BloraHat > ")

        if choice == '1':
            print("\n[*] Menjalankan Login Bypass Test...")
            if blora_riwayat.login():
                print("[SUCCESS] Bypass Captcha Berhasil. Token didapatkan.")
            else:
                print("[FAILED] Bypass Gagal.")
            input("\nTekan Enter untuk kembali...")
            
        elif choice == '2':
            start = int(input("[?] Range Awal: "))
            end = int(input("[?] Range Akhir: "))
            print(f"\n[*] Scanning No RM dari {start} ke {end}...")
            # Mode Scanner: Hanya cek nama tanpa ambil detail dalam
            blora_riwayat.run(start, end, mode="scanner")
            input("\nScanning Selesai. Tekan Enter...")

        elif choice == '3':
            start = int(input("[?] Range Awal: "))
            end = int(input("[?] Range Akhir: "))
            blora_reservasi.start_process(start, end)
            input("\nExtraction Selesai. Tekan Enter...")

        elif choice == '4':
            start = int(input("[?] Range Awal: "))
            end = int(input("[?] Range Akhir: "))
            blora_riwayat.run(start, end, mode="full")
            input("\nExtraction Selesai. Tekan Enter...")

        elif choice == '0':
            print("Happy Auditing!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")
            os.system('pause' if os.name == 'nt' else 'read')

if __name__ == "__main__":
    main_menu()