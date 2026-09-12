@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo WPOS PRO 2 - RELEASE BUILD
 echo ============================================================

where python >nul 2>&1
if errorlevel 1 goto :fail_python
python --version || goto :fail_python

if not exist "assets\branding\wpos_logo.png" goto :fail_logo
if not exist "assets\branding\wpos_icon.ico" goto :fail_icon
if not exist "run.py" goto :fail_run
if not exist "requirements.txt" goto :fail_requirements

for /f "delims=" %%V in ('python -c "from app.config import APP_VERSION; print(APP_VERSION)" 2^>nul') do set "APP_VERSION=%%V"
if not defined APP_VERSION goto :fail_version

python -c "import re,sys; v='!APP_VERSION!'; sys.exit(0 if re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', v) else 1)"
if errorlevel 1 goto :fail_version_format

set "EXE_NAME=WPOS_PRO_2_!APP_VERSION!.exe"
set "DIST_DIR=dist\WPOS PRO 2"
set "EXE_PATH=!DIST_DIR!\WPOS PRO 2.exe"
set "VERSIONED_EXE=dist\!EXE_NAME!"

 echo Version: !APP_VERSION!
echo.
echo [1/8] Checking dependencies...
python -m pip --version >nul 2>&1 || goto :fail_pip
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto :fail_dependencies

 echo [2/8] Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

 echo [3/8] Compile source...
python -m compileall -q app
if errorlevel 1 goto :fail_compile

 echo [4/8] Running regression tests...
set "PYTHONPATH=."
set "QT_QPA_PLATFORM=offscreen"
pytest -q
if errorlevel 1 goto :fail_tests

 echo [5/8] Building EXE with PyInstaller...
python -m PyInstaller --clean --noconfirm --windowed --icon "assets\branding\wpos_icon.ico" --name "WPOS PRO 2" --paths . --add-data "assets\branding\wpos_logo.png;assets\branding" --add-data "assets\branding\wpos_icon.ico;assets\branding" run.py
if errorlevel 1 goto :fail_pyinstaller

 echo [6/8] Validating EXE and packaged assets...
if not exist "!EXE_PATH!" goto :fail_exe
if not exist "!DIST_DIR!\_internal\assets\branding\wpos_logo.png" goto :fail_packaged_logo
if not exist "!DIST_DIR!\_internal\assets\branding\wpos_icon.ico" goto :fail_packaged_icon

copy /y "!EXE_PATH!" "!VERSIONED_EXE!" >nul
if errorlevel 1 goto :fail_copy

 echo [7/8] Validating version consistency...
python -c "from pathlib import Path; import re; from app.config import APP_VERSION; readme=Path('README.md').read_text(encoding='utf-8'); changelog=Path('CHANGELOG.md').read_text(encoding='utf-8') if Path('CHANGELOG.md').exists() else ''; expected=APP_VERSION; ok=(re.search(r'Versi aplikasi:\s*\*\*'+re.escape(expected)+r'\*\*',readme) is not None and re.search(r'^##?\s*'+re.escape(expected)+r'\b',changelog,re.M) is not None); print('Version gate:', expected); raise SystemExit(0 if ok else 1)"
if errorlevel 1 goto :fail_version_gate

 echo [8/8] Creating SHA-256 checksum...
certutil -hashfile "!VERSIONED_EXE!" SHA256 > "!VERSIONED_EXE!.sha256.txt"
if errorlevel 1 goto :fail_checksum

 echo.
echo ============================================================
echo BUILD BERHASIL
 echo ============================================================
echo Version : !APP_VERSION!
echo EXE     : !VERSIONED_EXE!
echo SHA256  : !VERSIONED_EXE!.sha256.txt
echo.
echo Catatan: data aplikasi EXE berada di %%LOCALAPPDATA%%\WPOS PRO 2.
echo ============================================================
exit /b 0

:fail_python
echo [ERROR] Python tidak ditemukan atau tidak dapat dijalankan.
goto :fail
:fail_logo
echo [ERROR] Logo branding tidak ditemukan: assets\branding\wpos_logo.png
goto :fail
:fail_icon
echo [ERROR] Icon aplikasi tidak ditemukan: assets\branding\wpos_icon.ico
goto :fail
:fail_run
echo [ERROR] run.py tidak ditemukan.
goto :fail
:fail_requirements
echo [ERROR] requirements.txt tidak ditemukan.
goto :fail
:fail_version
echo [ERROR] APP_VERSION tidak dapat dibaca dari app.config.
goto :fail
:fail_version_format
echo [ERROR] APP_VERSION bukan Semantic Versioning MAJOR.MINOR.PATCH.
goto :fail
:fail_pip
echo [ERROR] pip tidak tersedia.
goto :fail
:fail_dependencies
echo [ERROR] Instalasi dependency gagal.
goto :fail
:fail_compile
echo [ERROR] compileall gagal.
goto :fail
:fail_tests
echo [ERROR] Regression test gagal. Build dihentikan.
goto :fail
:fail_pyinstaller
echo [ERROR] PyInstaller gagal.
goto :fail
:fail_exe
echo [ERROR] EXE tidak ditemukan setelah build.
goto :fail
:fail_packaged_logo
echo [ERROR] Branding logo tidak ikut ter-package.
goto :fail
:fail_packaged_icon
echo [ERROR] Icon tidak ikut ter-package.
goto :fail
:fail_copy
echo [ERROR] Gagal membuat EXE versioned.
goto :fail
:fail_version_gate
echo [ERROR] README/CHANGELOG tidak sinkron dengan APP_VERSION.
goto :fail
:fail_checksum
echo [ERROR] SHA-256 gagal dibuat.
goto :fail

:fail
echo.
echo ============================================================
echo BUILD GAGAL - RELEASE GATE BERHENTI
 echo ============================================================
exit /b 1
