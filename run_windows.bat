@echo off
REM Quick Launch - Automated Data Broker Opt-Out Tool (Windows)

cd /d "%~dp0"

echo ==========================================
echo Data Broker Automated Opt-Out Tool
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Selenium is installed
python -c "import selenium" >nul 2>&1
if %errorlevel% neq 0 (
    echo Selenium not found. Running installer...
    call install_windows.bat
)

echo.
echo Starting automated opt-out tool...
echo.
python auto_optout_windows.py

pause
