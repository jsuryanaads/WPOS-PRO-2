@echo off
setlocal
cd /d "%~dp0"
echo === WPOS PRO V2 BUILD ===
python --version || (echo Python tidak ditemukan. & pause & exit /b 1)
if not exist assets\branding\wpos.png (echo Logo WPOS V2 tidak ditemukan. & pause & exit /b 1)
if not exist assets\branding\wpos.ico (echo Icon WPOS V2 tidak ditemukan. & pause & exit /b 1)
python -m pip install -r requirements.txt pyinstaller || goto fail
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
python -m PyInstaller --clean --noconfirm --windowed --icon "assets\branding\wpos.ico" --name "WPOS PRO V2" --paths . --add-data "assets\branding\wpos.png;assets\branding" --add-data "assets\branding\wpos.ico;assets\branding" run.py || goto fail
if not exist "dist\WPOS PRO V2\WPOS PRO V2.exe" goto fail
if not exist "dist\WPOS PRO V2\_internal\assets\branding\wpos.png" goto fail
if not exist "dist\WPOS PRO V2\_internal\assets\branding\wpos.ico" goto fail
echo.
echo BUILD BERHASIL: dist\WPOS PRO V2\WPOS PRO V2.exe
echo Windows icon: assets\branding\wpos.ico
echo Branding logo: dist\WPOS PRO V2\_internal\assets\branding\wpos.png
echo.
echo Catatan: data aplikasi disimpan di %%LOCALAPPDATA%%\WPOS PRO V2 saat dijalankan sebagai EXE.
pause
exit /b 0
:fail
echo BUILD GAGAL.
pause
exit /b 1
