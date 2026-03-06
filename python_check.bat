@echo off
REM RouteMaster AI - Python Setup Check
REM This script verifies and fixes Python installation

echo.
echo ========================================
echo   Python Installation Check
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Python is installed!
    echo.
    python --version
    echo.
    pip --version
    echo.
    echo Next steps:
    echo 1. Run: pip install -r requirements.txt
    echo 2. Run: python app.py
    echo 3. Open: http://localhost:8000
    echo.
    pause
    exit /b 0
)

REM Python not found - provide guidance
echo [ERROR] Python is NOT installed or not in PATH
echo.
echo Solution: Install Python 3.11+ from https://www.python.org/downloads/
echo.
echo IMPORTANT: During installation, check the box:
echo   "Add Python to PATH"
echo.
echo After installation:
echo   1. Close and reopen this terminal
echo   2. Run this script again
echo   3. If still failing, run: python_fix_path.bat
echo.

REM Try to find Python in common locations
echo Searching for Python installations...
echo.

set "python_found=0"

if exist "C:\Program Files\Python311\python.exe" (
    echo Found: C:\Program Files\Python311
    set "python_found=1"
    goto found_python
)

if exist "C:\Program Files\Python312\python.exe" (
    echo Found: C:\Program Files\Python312
    set "python_found=1"
    goto found_python
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    echo Found: %LOCALAPPDATA%\Programs\Python\Python311
    set "python_found=1"
    goto found_python
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    echo Found: %LOCALAPPDATA%\Programs\Python\Python312
    set "python_found=1"
    goto found_python
)

echo No Python installations found in standard locations.
echo.
echo Download Python from: https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation
echo.
pause
exit /b 1

:found_python
echo.
echo Python FOUND! Adding to PATH...
setx PATH "%CD:\=\\%;!%PATH%!"

echo.
echo [SUCCESS] Python has been added to PATH
echo Please restart this terminal and try again
echo.
pause
