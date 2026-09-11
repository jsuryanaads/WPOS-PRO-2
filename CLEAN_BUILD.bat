@echo off
cd /d "%~dp0"
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --clean --noconfirm --windowed --name "WPOS PRO" app\main.py
if errorlevel 1 goto fail
echo BUILD PASS
echo dist\WPOS PRO.exe
pause
exit /b 0
:fail
echo BUILD FAIL
pause
