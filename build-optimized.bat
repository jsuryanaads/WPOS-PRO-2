@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

REM ============================================================
REM WPOS PRO 2 - OPTIMIZED BUILD SCRIPT
REM ============================================================
REM
REM Usage:
REM   build-optimized.bat dev     - Fast iteration (50s, no tests)
REM   build-optimized.bat ci      - Parallel tests (90s, pre-release)
REM   build-optimized.bat release - Full validation (120s, production)
REM   build-optimized.bat         - Defaults to 'release'
REM
REM ============================================================

if "%~1"=="" set "BUILD_MODE=release"
else set "BUILD_MODE=%~1"

echo.
echo ============================================================
echo WPOS PRO 2 - OPTIMIZED BUILD [!BUILD_MODE!]
echo ============================================================
echo.

REM Pre-flight checks
where python >nul 2>&1
if errorlevel 1 goto :fail_python
python --version || goto :fail_python

if not exist "assets\branding\wpos_logo.png" goto :fail_logo
if not exist "assets\branding\wpos_icon.ico" goto :fail_icon
if not exist "run.py" goto :fail_run
if not exist "requirements.txt" goto :fail_requirements

REM Extract version
for /f "delims=" %%V in ('python -c "from app.config import APP_VERSION; print(APP_VERSION)" 2^>nul') do set "APP_VERSION=%%V"
if not defined APP_VERSION goto :fail_version

python -c "import re,sys; v='!APP_VERSION!'; sys.exit(0 if re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', v) else 1)"
if errorlevel 1 goto :fail_version_format

set "EXE_NAME=WPOS_PRO_2_!APP_VERSION!.exe"
set "DIST_DIR=dist\WPOS PRO 2"
set "EXE_PATH=!DIST_DIR!\WPOS PRO 2.exe"
set "VERSIONED_EXE=dist\!EXE_NAME!"

echo Version: !APP_VERSION!
echo Mode: !BUILD_MODE!
echo.

REM ========== STAGE 1: Dependencies (with pip cache) ==========
echo [1/6] Checking and installing dependencies...
python -m pip --version >nul 2>&1 || goto :fail_pip
python -m pip install --upgrade pip setuptools >nul 2>&1
python -m pip install -r requirements.txt pyinstaller --prefer-binary -q
if errorlevel 1 goto :fail_dependencies
echo [OK] Dependencies ready

REM ========== STAGE 2: Clean build artifacts ==========
echo [2/6] Cleaning previous build artifacts...
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1
echo [OK] Build directory cleaned

REM ========== DEV MODE: Skip tests, quick package ==========
if "%BUILD_MODE%"=="dev" (
  echo.
  echo [DEV MODE] Skipping test validation...
  goto :stage_5_dev
)

REM ========== STAGE 3: Tests (parallel for ci/release) ==========
echo [3/6] Running regression tests...

python -m pip install pytest-xdist -q >nul 2>&1

set "PYTHONPATH=."
set "QT_QPA_PLATFORM=offscreen"

if "%BUILD_MODE%"=="ci" (
  REM Parallel execution for CI pipeline
  pytest -q -n auto --dist loadscope
) else (
  REM Sequential for release (more stable)
  pytest -q
)

if errorlevel 1 goto :fail_tests
echo [OK] All tests passed

REM ========== STAGE 5: PyInstaller (optimized) ==========
:stage_5_dev
echo [4/6] Building EXE with PyInstaller...

REM Use --clean only for release mode (full validation needed)
set "PYINSTALLER_FLAGS=--noconfirm --windowed --icon "assets\branding\wpos_icon.ico" --name "WPOS PRO 2" --paths ."
set "PYINSTALLER_DATA=--add-data "assets\branding\wpos_logo.png;assets\branding" --add-data "assets\branding\wpos_icon.ico;assets\branding""

if "%BUILD_MODE%"=="release" (
  python -m PyInstaller --clean %PYINSTALLER_FLAGS% %PYINSTALLER_DATA% run.py
) else (
  REM Keep the build invocation lightweight for dev/ci
  python -m PyInstaller %PYINSTALLER_FLAGS% %PYINSTALLER_DATA% run.py
)

if errorlevel 1 goto :fail_pyinstaller
echo [OK] EXE packaging complete

REM ========== STAGE 6: Validation & Output ==========
echo [5/6] Validating build artifacts...

if not exist "!EXE_PATH!" goto :fail_exe
if not exist "!DIST_DIR!\_internal\assets\branding\wpos_logo.png" goto :fail_packaged_logo
if not exist "!DIST_DIR!\_internal\assets\branding\wpos_icon.ico" goto :fail_packaged_icon

copy /y "!EXE_PATH!" "!VERSIONED_EXE!" >nul
if errorlevel 1 goto :fail_copy

echo [OK] Artifacts validated

REM ========== STAGE 7: Version Gate (release mode only) ==========
if "%BUILD_MODE%"=="release" (
  echo [6/6] Validating version consistency...
  python -c "from pathlib import Path; import re; from app.config import APP_VERSION; readme=Path('README.md').read_text(encoding='utf-8'); changelog=Path('CHANGELOG.md').read_text(encoding='utf-8'); assert APP_VERSION in readme, 'README mismatch'; assert APP_VERSION in changelog, 'CHANGELOG mismatch'; print('[OK] Version gates passed')"
  if errorlevel 1 goto :fail_version_gate
  
  certutil -hashfile "!VERSIONED_EXE!" SHA256 > "!VERSIONED_EXE!.sha256.txt"
  if errorlevel 1 goto :fail_checksum
) else (
  echo [6/6] Skipping version gate ^(dev/ci mode^)
)

REM ========== BUILD SUCCESS ==========
echo.
echo ============================================================
echo BUILD BERHASIL [!BUILD_MODE!]
echo ============================================================
echo Version : !APP_VERSION!
echo EXE     : !VERSIONED_EXE!
if "%BUILD_MODE%"=="release" (
  echo SHA256  : !VERSIONED_EXE!.sha256.txt
)
echo.
echo Catatan: Data aplikasi EXE berada di %%LOCALAPPDATA%%\WPOS PRO 2
echo ============================================================
exit /b 0

REM ========== ERROR HANDLERS ==========
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
