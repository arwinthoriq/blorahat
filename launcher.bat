@echo off
title BloraHat Security Tool - Auto Launcher
cls

:: 1. Cek apakah Python terinstal
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python tidak terdeteksi di sistem Anda.
    echo [*] Mencoba menginstal Python secara otomatis via Winget...
    winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements
    if %errorlevel% neq 0 (
        echo [-] Gagal menginstal Python otomatis. 
        echo [!] Silakan unduh Python secara manual di: https://www.python.org/downloads/
        echo [!] Pastikan centang 'Add Python to PATH' saat instalasi.
        pause
        exit
    )
    echo [+] Python berhasil diinstal! Silakan buka kembali file launcher ini.
    pause
    exit
)

set SCRIPT_NAME=main.py

:: 3. Jalankan pembersihan PIP dan instalasi requirements
echo [*] Mengecek dependensi dan library...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt >nul 2>&1

:: 4. Jalankan Tool
echo [+] Menjalankan BloraHat...
python %SCRIPT_NAME%
pause