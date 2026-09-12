@echo off
setlocal
cd /d "%~dp0"
echo === WPOS PRO 2 BUILD ===
python --version || (echo Python tidak ditemukan. & pause & exit /b 1)
if not exist assets\branding\wpos_logo.png (echo Logo WPOS PRO 2 tidak ditemukan: wpos_logo.png & pause & exit /b 1)
if not exist assets\branding\wpos_icon.ico (echo Icon WPOS PRO 2 tidak ditemukan: wpos_icon.ico & pause & exit /b 1)
for /f "delims=" %%V in ('python -c "from app.config import APP_VERSION; print(APP_VERSION)"') do set "APP_VERSION=%%V"
if "%APP_VERSION%"=="" (echo APP_VERSION tidak dapat dibaca. & pause & exit /b 1)
echo Version: %APP_VERSION%
python -m pip install -r requirements.txt pyinstaller || goto fail
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
python -m compileall -q app || goto fail
set "PYTHONPATH=."
set "QT_QPA_PLATFORM=offscreen"
pytest -q || goto fail
python -m PyInstaller --clean --noconfirm --windowed --icon "assets\branding\wpos_icon.ico" --name "WPOS PRO 2" --paths . --add-data "assets\branding\wpos_logo.png;assets\branding" --add-data "assets\branding\wpos_icon.ico;assets\branding" run.py || goto fail
if not exist "dist\WPOS PRO 2\WPOS PRO 2.exe" goto fail
if not exist "dist\WPOS PRO 2\_internal\assets\branding\wpos_logo.png" goto fail
if not exist "dist\WPOS PRO 2\_internal\assets\branding\wpos_icon.ico" goto fail
copy /y "dist\WPOS PRO 2\WPOS PRO 2.exe" "dist\WPOS_PRO_2_%APP_VERSION%.exe" >nul || goto fail
echo.
echo BUILD BERHASIL: dist\WPOS_PRO_2_%APP_VERSION%.exe
echo Version: %APP_VERSION%
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
