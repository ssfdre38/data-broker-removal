# Data Broker Removal Tool

A cross-platform tool to help you remove your personal information from major data brokers all at once.

**📘 Windows Users:** See [README_WINDOWS.md](README_WINDOWS.md) for detailed Windows instructions and batch files.

## What This Tool Does

- Generates a CCPA/GDPR compliant email template for removal requests
- Creates an interactive HTML checklist with direct links to opt-out pages
- Tracks your progress as you submit removal requests
- Includes 25+ major data brokers

## Quick Start

### Option 1: Manual Process (Recommended First)

```bash
cd ~/data-broker-removal
python3 remove_data.py
```

This generates checklists and templates you use manually.

### Option 2: Automated Process (Semi-Automated)

```bash
cd ~/data-broker-removal
# Install dependencies first (one-time)
bash install_selenium.sh

# Run automated tool
python3 auto_optout.py
```

This opens a browser and helps automate form filling, but still requires your interaction for CAPTCHAs and verification steps.

### What You'll Need

- Your full name
- Email address
- Optionally: address, city, state, ZIP, phone number

### Output Files

The tool generates three files in the `output/` directory:

1. **email_template_[timestamp].txt** - Email template to send to data brokers
2. **removal_checklist_[timestamp].html** - Interactive checklist (open in browser)
3. **removal_checklist_[timestamp].txt** - Printable text version

## How to Use

### Step 1: Generate Your Files

Run the script and enter your information when prompted:

```bash
python3 remove_data.py
```

### Step 2: Open the HTML Checklist

Open the generated HTML file in your web browser. This gives you:
- Direct links to each broker's opt-out page
- Checkboxes to track progress
- Progress bar showing completion percentage
- Your information saved locally (persists across browser sessions)

### Step 3: Visit Each Opt-Out Page

For each data broker:
1. Click "Visit Opt-Out Page"
2. Search for your information on their site (most require this first)
3. Follow their removal process
4. Check the box when complete

### Step 4: Track Confirmations

- Most brokers send confirmation emails
- Process can take up to 45 days (legal requirement)
- Follow up if you don't hear back

## Data Brokers Included

The tool includes 25+ major data brokers:

**People Search Sites:**
- Spokeo
- WhitePages
- BeenVerified
- Intelius
- PeopleFinders
- Instant Checkmate
- TruthFinder
- TruePeopleSearch
- FastPeopleSearch
- And more...

**Data Aggregators:**
- Acxiom
- Experian
- Oracle Data Cloud

## Important Notes

### Opt-Out Process Varies

Each data broker has their own process:
- **Web forms**: Most common - fill out and submit
- **Email requests**: Send your removal template
- **Photo ID required**: Some may ask for ID verification
- **Search first**: Most require finding your listing before removal

### Legal Rights

This tool helps you exercise rights under:
- **CCPA** (California Consumer Privacy Act)
- **GDPR** (General Data Protection Regulation)
- **Other state privacy laws**

Data brokers must respond within 45 days by law.

### What to Expect

- ✅ Most removals are free
- ⏱️ Takes 1-3 hours to submit all requests
- 📧 You'll receive confirmation emails
- 🔄 Some data may reappear (requires periodic maintenance)

## Tips for Success

1. **Use a dedicated email** - Create a new email just for this to avoid spam
2. **Take screenshots** - Document each submission
3. **Keep a log** - Note submission dates and confirmation numbers
4. **Be patient** - Full removal can take 1-2 months
5. **Repeat quarterly** - Data can be re-added from public records
6. **Check social media** - Remove personal info from your profiles too

## Troubleshooting

### Can't find yourself on a site?
- Try variations of your name
- Use old addresses
- Try phone number searches
- You might not be listed (that's good!)

### Site won't accept removal?
- Take screenshots
- File complaint with your state AG
- CCPA violations can result in fines

### Email template not working?
- Customize it for specific brokers
- Keep it professional and cite CCPA/GDPR

## Advanced Usage

### Add Custom Data Brokers

Edit `data_brokers.json` to add more:

```json
{
  "name": "BrokerName",
  "website": "https://example.com",
  "opt_out_url": "https://example.com/opt-out",
  "method": "web_form",
  "email": "privacy@example.com"
}
```

### Customize Email Template

Edit the `generate_email_template()` function in `remove_data.py`.

## Privacy Notice

This tool runs completely offline and doesn't send any data anywhere. All information stays on your computer.

## Additional Resources

- [Privacy Rights Clearinghouse](https://privacyrights.org/)
- [CCPA Information](https://oag.ca.gov/privacy/ccpa)
- [FTC Identity Theft Guide](https://www.identitytheft.gov/)

## Automated vs Manual

### Manual Process (`remove_data.py`)
**Pros:**
- ✓ No dependencies needed
- ✓ Complete control
- ✓ Works on any system
- ✓ Generates helpful templates

**Cons:**
- ✗ Time-consuming (1-3 hours)
- ✗ Repetitive form filling

### Automated Process (`auto_optout.py`)
**Pros:**
- ✓ Semi-automated form filling
- ✓ Auto-screenshots for records
- ✓ Progress tracking
- ✓ Batch processing

**Cons:**
- ✗ Requires Selenium + ChromeDriver
- ✗ Still needs manual CAPTCHA solving
- ✗ Some sites detect automation
- ✗ More complex setup

**Recommendation:** Start with the manual tool to understand the process, then use automation for quarterly maintenance.

## Support

This tool is provided as-is to help protect your privacy. For legal questions, consult a privacy attorney.

---

**Remember:** Removing your data from brokers is an ongoing process. Set a calendar reminder to repeat this quarterly!
