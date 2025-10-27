# Data Broker Removal Tool - Windows Guide

Complete guide for Windows users to remove their data from data brokers.

## 📥 Installation (Windows)

### Prerequisites

1. **Install Python** (if not already installed):
   - Download from: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
   - Restart your computer after installation

2. **Download this tool**:
   - Download all files to a folder (e.g., `C:\DataBrokerRemoval`)

### Setup

**Double-click:** `install_windows.bat`

This will:
- Install Python Selenium library
- Optionally install webdriver-manager for automatic ChromeDriver setup
- Guide you through ChromeDriver installation

## 🚀 Quick Start (Windows)

### Option 1: Manual Process (Easiest)

**Double-click:** `run_manual_windows.bat`

This creates:
- Interactive HTML checklist
- Email templates
- Printable tracking sheet

No browser automation needed.

### Option 2: Automated Process

**Double-click:** `run_windows.bat`

This opens a browser and helps you submit opt-out requests automatically.

## 📋 Detailed Instructions

### Manual Process

1. Double-click `run_manual_windows.bat`
2. Enter your information when prompted
3. Open the generated HTML file in your browser
4. Click through each data broker's opt-out link
5. Check boxes as you complete each one

**Files generated in `output\` folder:**
- `removal_checklist_[timestamp].html` - Interactive checklist
- `email_template_[timestamp].txt` - Email template
- `removal_checklist_[timestamp].txt` - Printable version

### Automated Process

1. **First time only:**
   - Double-click `install_windows.bat`
   - Choose to install webdriver-manager (recommended)
   
2. **Run the tool:**
   - Double-click `run_windows.bat`
   - Enter your information
   - Choose whether to show browser (recommended: No for first run)
   
3. **During automation:**
   - Browser will open automatically
   - Tool navigates to each opt-out page
   - Auto-fills forms when possible
   - Pauses for you to complete CAPTCHAs
   - Takes screenshots for your records
   
4. **After each broker:**
   - Press Enter to continue
   - Or type 'q' to quit
   
**Logs saved in `logs\` folder:**
- Screenshots of each step
- JSON report of all results

## 🔧 Troubleshooting (Windows)

### "Python is not recognized"

**Solution:**
1. Uninstall Python
2. Reinstall from python.org
3. ✅ Check "Add Python to PATH"
4. Restart computer

### "ChromeDriver not found"

**Option A: Automatic (Recommended)**
```cmd
pip install webdriver-manager
```

**Option B: Manual**
1. Check your Chrome version: `chrome://settings/help`
2. Download matching ChromeDriver: https://chromedriver.chromium.org/
3. Extract `chromedriver.exe` to the tool folder

### "Selenium not found"

```cmd
pip install selenium
```

### Permission Issues

**Run as Administrator:**
- Right-click `install_windows.bat`
- Select "Run as administrator"

### Firewall Blocking

- Allow Python through Windows Firewall when prompted
- Allow Chrome/ChromeDriver through firewall

## 💡 Windows-Specific Tips

### 1. Use Edge Instead of Chrome

If you use Microsoft Edge, you need EdgeDriver:
```cmd
pip install msedge-selenium-tools
```

### 2. Running from Command Prompt

```cmd
cd C:\path\to\data-broker-removal
python remove_data.py
```

Or for automated:
```cmd
python auto_optout_windows.py
```

### 3. Scheduled Task (Quarterly Reminders)

Create a scheduled task to remind you quarterly:

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Data Broker Removal Reminder"
4. Trigger: Quarterly
5. Action: Display a message or run `run_manual_windows.bat`

### 4. Virtual Environment (Optional)

For clean Python environment:
```cmd
python -m venv venv
venv\Scripts\activate
pip install selenium webdriver-manager
python auto_optout_windows.py
```

## 📁 File Structure

```
data-broker-removal\
├── remove_data.py              - Manual tool (cross-platform)
├── auto_optout_windows.py      - Automated tool (Windows-optimized)
├── data_brokers.json           - List of 25+ data brokers
├── install_windows.bat         - Windows installer
├── run_manual_windows.bat      - Launch manual tool
├── run_windows.bat             - Launch automated tool
├── README_WINDOWS.md           - This file
├── output\                     - Generated checklists/templates
└── logs\                       - Screenshots and results
```

## 🎯 What Each File Does

| File | Purpose | When to Use |
|------|---------|-------------|
| `run_manual_windows.bat` | Creates checklists you fill out manually | First time / prefer control |
| `run_windows.bat` | Automates browser navigation | After understanding process |
| `install_windows.bat` | Sets up dependencies | One-time setup |
| `auto_optout_windows.py` | Main automation script | Advanced users |
| `remove_data.py` | Manual checklist generator | Any platform |

## ⚙️ Advanced Options

### Command Line Arguments

For power users, you can modify the scripts to accept command-line arguments:

```cmd
python auto_optout_windows.py --headless --fast
```

### Custom Data Broker List

Edit `data_brokers.json` to add or remove brokers:
```json
{
  "name": "NewBroker",
  "website": "https://example.com",
  "opt_out_url": "https://example.com/optout",
  "method": "web_form",
  "email": null
}
```

## 🛡️ Privacy & Security

- ✅ All processing happens locally on your PC
- ✅ No data is sent to third parties
- ✅ Screenshots stored locally only
- ✅ You control what information to provide
- ✅ Open source - review the code yourself

## 📞 Common Questions

**Q: Do I need Chrome installed?**
A: Yes, or you can modify for Edge/Firefox

**Q: Will this work on Windows 7?**
A: Yes, but Python 3.9+ and Chrome must be compatible

**Q: Can I run this on a work computer?**
A: Check with IT first - may need admin rights

**Q: How long does automation take?**
A: 45-90 minutes for all 25+ brokers

**Q: Is this safe?**
A: Yes, but review the code yourself. It's open source.

**Q: Will brokers know I'm automating?**
A: Some may detect it. Use manual mode if needed.

## 🆘 Getting Help

1. **Check logs folder** - Look for error screenshots
2. **Run in visible mode** - See what's happening
3. **Use manual mode** - Guaranteed to work
4. **Check Python version** - Need 3.7 or higher
5. **Update Chrome** - Match ChromeDriver version

## 📚 Additional Resources

- Python Download: https://www.python.org/downloads/
- ChromeDriver: https://chromedriver.chromium.org/
- Selenium Docs: https://selenium-python.readthedocs.io/
- CCPA Info: https://oag.ca.gov/privacy/ccpa

## ✅ Quick Checklist

Before running:
- [ ] Python installed with PATH added
- [ ] Downloaded all tool files
- [ ] Ran `install_windows.bat`
- [ ] Chrome or Edge browser installed
- [ ] ChromeDriver installed (or webdriver-manager)

To use:
- [ ] Double-click `run_manual_windows.bat` OR
- [ ] Double-click `run_windows.bat`
- [ ] Enter your information
- [ ] Follow prompts

---

**Need help?** Start with the manual process (`run_manual_windows.bat`) - it's foolproof and requires no setup beyond Python.
