@echo off
REM Quick Launch - Manual Data Broker Removal Tool (Windows)

cd /d "%~dp0"

echo ==========================================
echo Data Broker Removal Request Generator
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

echo Starting removal request generator...
echo.
python remove_data.py

pause
