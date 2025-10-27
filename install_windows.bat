@echo off
REM Data Broker Removal Tool - Windows Installation Script

echo ==========================================
echo Installing Selenium and ChromeDriver
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Installing Selenium...
python -m pip install --upgrade pip
python -m pip install selenium

echo.
echo ==========================================
echo ChromeDriver Installation
echo ==========================================
echo.
echo You have two options:
echo.
echo Option 1: Manual Installation (Recommended)
echo   1. Download ChromeDriver from: https://chromedriver.chromium.org/
echo   2. Match your Chrome browser version
echo   3. Extract chromedriver.exe to this folder or add to PATH
echo.
echo Option 2: Automatic (using webdriver-manager)
echo   Will automatically download and manage ChromeDriver
echo.

set /p choice="Install webdriver-manager for automatic ChromeDriver? (y/n): "
if /i "%choice%"=="y" (
    echo Installing webdriver-manager...
    python -m pip install webdriver-manager
    echo.
    echo ✓ webdriver-manager installed
    echo   The tool will automatically download ChromeDriver when needed
) else (
    echo.
    echo Please download ChromeDriver manually:
    echo   1. Visit: https://chromedriver.chromium.org/downloads
    echo   2. Download the version matching your Chrome browser
    echo   3. Extract chromedriver.exe to: %~dp0
    echo.
)

echo.
echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo To run the tools:
echo   Manual process:    python remove_data.py
echo   Automated process: python auto_optout.py
echo.
pause
