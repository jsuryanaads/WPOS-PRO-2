@echo off
setlocal
cd /d "%~dp0"
echo === WPOS PRO 2 BUILD ===
python --version || (echo Python tidak ditemukan. & pause & exit /b 1)
if not exist assets\branding\wpos_logo.png (echo Logo WPOS PRO 2 tidak ditemukan: wpos_logo.png & pause & exit /b 1)
if not exist assets\branding\wpos_icon.ico (echo Icon WPOS PRO 2 tidak ditemukan: wpos_icon.ico & pause & exit /b 1)
python -m pip install -r requirements.txt pyinstaller || goto fail
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
python -m PyInstaller --clean --noconfirm --windowed --icon "assets\branding\wpos_icon.ico" --name "WPOS PRO 2" --paths . --add-data "assets\branding\wpos_logo.png;assets\branding" --add-data "assets\branding\wpos_icon.ico;assets\branding" run.py || goto fail
if not exist "dist\WPOS PRO 2\WPOS PRO 2.exe" goto fail
if not exist "dist\WPOS PRO 2\_internal\assets\branding\wpos_logo.png" goto fail
if not exist "dist\WPOS PRO 2\_internal\assets\branding\wpos_icon.ico" goto fail
echo.
echo BUILD BERHASIL: dist\WPOS PRO 2\WPOS PRO 2.exe
echo Windows icon: assets\branding\wpos_icon.ico
echo Branding logo: dist\WPOS PRO 2\_internal\assets\branding\wpos_logo.png
echo.
echo Catatan: data aplikasi disimpan di %%LOCALAPPDATA%%\WPOS PRO 2 saat dijalankan sebagai EXE.
pause
exit /b 0
:fail
echo BUILD GAGAL.
pause
exit /b 1
