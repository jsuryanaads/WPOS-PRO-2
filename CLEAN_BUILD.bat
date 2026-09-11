@echo off
setlocal
cd /d "%~dp0"
echo === WPOS PRO 2 CLEAN BUILD ===
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
python --version || (echo Python tidak ditemukan. & pause & exit /b 1)
if not exist assets\branding\wpos_logo.png (echo Logo tidak ditemukan: wpos_logo.png & pause & exit /b 1)
if not exist assets\branding\wpos_icon.ico (echo Icon tidak ditemukan: wpos_icon.ico & pause & exit /b 1)
python -m pip install -r requirements.txt pyinstaller || goto fail
python -m PyInstaller --clean --noconfirm --windowed --icon "assets\branding\wpos_icon.ico" --name "WPOS PRO 2" --paths . --add-data "assets\branding\wpos_logo.png;assets\branding" --add-data "assets\branding\wpos_icon.ico;assets\branding" run.py || goto fail
if not exist "dist\WPOS PRO 2\WPOS PRO 2.exe" goto fail
echo BUILD PASS
echo dist\WPOS PRO 2\WPOS PRO 2.exe
pause
exit /b 0
:fail
echo BUILD FAIL
pause
exit /b 1
