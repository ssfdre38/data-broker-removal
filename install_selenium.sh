#!/bin/bash

echo "=========================================="
echo "Installing Selenium and ChromeDriver"
echo "=========================================="
echo ""

# Install Python Selenium
echo "Installing Python Selenium..."
pip3 install selenium

# Install Chrome/Chromium and ChromeDriver
echo ""
echo "Installing Chromium and ChromeDriver..."

if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install -y chromium-browser chromium-chromedriver
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    sudo yum install -y chromium chromedriver
elif command -v pacman &> /dev/null; then
    # Arch
    sudo pacman -S chromium chromedriver
else
    echo "⚠️  Could not detect package manager."
    echo "Please install chromium and chromedriver manually:"
    echo "  - Download ChromeDriver from: https://chromedriver.chromium.org/"
    echo "  - Install Chromium browser"
    exit 1
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "To run the automated opt-out tool:"
echo "  python3 auto_optout.py"
echo ""
