@echo off
setlocal

REM Build MewRus.exe on Windows using PyInstaller

where py >nul 2>nul
if %errorlevel% neq 0 (
  echo [ERROR] Python launcher ^"py^" not found. Install Python for Windows first.
  exit /b 1
)

echo [1/3] Installing/updating PyInstaller...
py -m pip install --upgrade pyinstaller
if %errorlevel% neq 0 (
  echo [ERROR] Failed to install PyInstaller.
  exit /b 1
)

echo [2/3] Building MewRus.exe...
py -m PyInstaller --noconfirm --clean --windowed --onefile --name MewRus --icon NONE --add-data "payload;payload" MewRus.py
if %errorlevel% neq 0 (
  echo [ERROR] Build failed.
  exit /b 1
)

echo [3/3] Done.
echo EXE file: dist\MewRus.exe
exit /b 0
