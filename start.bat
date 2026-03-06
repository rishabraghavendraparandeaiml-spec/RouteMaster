@echo off
REM RouteMaster AI - Quick Start Script for Windows
REM This script automates the setup and testing process

echo.
echo ========================================
echo   RouteMaster AI - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo.

REM Get user choice
echo Select an option:
echo [1] Run compatibility tests (no server needed)
echo [2] Install dependencies
echo [3] Start FastAPI server
echo [4] Install + Start server
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Running compatibility tests...
    python test_compatibility.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    echo.
    echo [SUCCESS] Dependencies installed
    pause
) else if "%choice%"=="3" (
    echo.
    echo Starting FastAPI server...
    echo.
    echo Press CTRL+C to stop the server
    echo Open browser to: http://localhost:8000
    echo.
    python app.py
) else if "%choice%"=="4" (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
    echo [SUCCESS] Dependencies installed
    echo.
    echo Starting FastAPI server...
    echo.
    echo Press CTRL+C to stop the server
    echo Open browser to: http://localhost:8000
    echo.
    python app.py
) else (
    echo Invalid choice
    pause
)
