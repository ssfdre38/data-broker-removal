#!/usr/bin/env python3
"""
Automated Data Broker Opt-Out Tool
Uses Selenium to automate the opt-out process for data brokers
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AutoOptOutTool:
    def __init__(self, headless=False):
        self.script_dir = Path(__file__).parent
        self.data_file = self.script_dir / "data_brokers.json"
        self.log_dir = self.script_dir / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.brokers = self.load_brokers()
        self.driver = None
        self.headless = headless
        self.results = []
        
    def load_brokers(self):
        """Load data broker information"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.data_file} not found")
            sys.exit(1)
    
    def init_driver(self):
        """Initialize Chrome/Chromium driver"""
        print("Initializing browser...")
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✓ Browser initialized\n")
        except Exception as e:
            print(f"Error initializing browser: {e}")
            print("\nPlease install ChromeDriver:")
            print("  Ubuntu/Debian: sudo apt-get install chromium-chromedriver")
            print("  Or download from: https://chromedriver.chromium.org/")
            sys.exit(1)
    
    def close_driver(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
    
    def take_screenshot(self, broker_name, stage=""):
        """Take a screenshot for logging"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{broker_name.replace(' ', '_')}_{stage}_{timestamp}.png"
        filepath = self.log_dir / filename
        try:
            self.driver.save_screenshot(str(filepath))
            return str(filepath)
        except Exception as e:
            print(f"  Warning: Could not save screenshot: {e}")
            return None
    
    def wait_for_user(self, message):
        """Pause and wait for user to complete manual steps"""
        print(f"\n⏸️  {message}")
        input("Press Enter when ready to continue...")
    
    def process_spokeo(self, user_info):
        """Automated opt-out for Spokeo"""
        print("Processing Spokeo...")
        try:
            self.driver.get("https://www.spokeo.com/optout")
            time.sleep(3)
            self.take_screenshot("Spokeo", "landing")
            
            # User needs to search for themselves first
            self.wait_for_user("Please search for yourself on Spokeo and copy the URL of your profile")
            profile_url = input("Paste your Spokeo profile URL here: ").strip()
            
            if profile_url:
                # Try to fill opt-out form
                try:
                    url_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "url"))
                    )
                    url_input.send_keys(profile_url)
                    
                    email_input = self.driver.find_element(By.NAME, "email")
                    email_input.send_keys(user_info['email'])
                    
                    self.take_screenshot("Spokeo", "form_filled")
                    
                    self.wait_for_user("Please complete any CAPTCHA and click submit")
                    self.take_screenshot("Spokeo", "submitted")
                    
                    return {"status": "success", "message": "Opt-out submitted"}
                except Exception as e:
                    return {"status": "manual", "message": f"Requires manual completion: {e}"}
            else:
                return {"status": "skipped", "message": "No profile URL provided"}
                
        except Exception as e:
            self.take_screenshot("Spokeo", "error")
            return {"status": "error", "message": str(e)}
    
    def process_whitepages(self, user_info):
        """Automated opt-out for WhitePages"""
        print("Processing WhitePages...")
        try:
            self.driver.get("https://www.whitepages.com/suppression_requests")
            time.sleep(3)
            self.take_screenshot("WhitePages", "landing")
            
            self.wait_for_user("Please search for yourself on WhitePages and note your listing")
            
            # Try to automate form
            try:
                # Form fields vary, so this is semi-automated
                self.wait_for_user("Please fill out the opt-out form and submit")
                self.take_screenshot("WhitePages", "submitted")
                return {"status": "success", "message": "Opt-out submitted"}
            except Exception as e:
                return {"status": "manual", "message": f"Requires manual completion: {e}"}
                
        except Exception as e:
            self.take_screenshot("WhitePages", "error")
            return {"status": "error", "message": str(e)}
    
    def process_generic(self, broker, user_info):
        """Generic processor for brokers that need manual interaction"""
        print(f"Processing {broker['name']}...")
        try:
            self.driver.get(broker['opt_out_url'])
            time.sleep(3)
            self.take_screenshot(broker['name'], "landing")
            
            # Try to auto-fill common form fields
            try:
                # Look for common field names
                common_name_fields = ['name', 'full_name', 'fullname', 'fname', 'first_name']
                common_email_fields = ['email', 'email_address', 'e-mail']
                
                for field_name in common_name_fields:
                    try:
                        field = self.driver.find_element(By.NAME, field_name)
                        field.send_keys(user_info['name'])
                        print(f"  ✓ Filled name field")
                        break
                    except NoSuchElementException:
                        continue
                
                for field_name in common_email_fields:
                    try:
                        field = self.driver.find_element(By.NAME, field_name)
                        field.send_keys(user_info['email'])
                        print(f"  ✓ Filled email field")
                        break
                    except NoSuchElementException:
                        continue
                
                self.take_screenshot(broker['name'], "form_filled")
                
            except Exception as e:
                print(f"  Could not auto-fill: {e}")
            
            # Ask user to complete
            self.wait_for_user(f"Please complete the opt-out process for {broker['name']}")
            self.take_screenshot(broker['name'], "completed")
            
            return {"status": "success", "message": "Opt-out process completed"}
            
        except Exception as e:
            self.take_screenshot(broker['name'], "error")
            return {"status": "error", "message": str(e)}
    
    def run_automated_optout(self, user_info, broker_list=None):
        """Run automated opt-out for all brokers"""
        if broker_list is None:
            broker_list = self.brokers
        
        print("\n" + "="*80)
        print("AUTOMATED DATA BROKER OPT-OUT")
        print("="*80)
        print(f"\nProcessing {len(broker_list)} data brokers")
        print(f"User: {user_info['name']} ({user_info['email']})")
        print("\nNote: Many sites require you to search for yourself first")
        print("Screenshots will be saved to:", self.log_dir)
        print("\n" + "="*80 + "\n")
        
        self.init_driver()
        
        for idx, broker in enumerate(broker_list, 1):
            print(f"\n[{idx}/{len(broker_list)}] {broker['name']}")
            print("-" * 80)
            
            # Special handlers for specific brokers
            if broker['name'] == "Spokeo":
                result = self.process_spokeo(user_info)
            elif broker['name'] == "WhitePages":
                result = self.process_whitepages(user_info)
            else:
                result = self.process_generic(broker, user_info)
            
            result['broker'] = broker['name']
            result['timestamp'] = datetime.now().isoformat()
            self.results.append(result)
            
            print(f"  Status: {result['status']}")
            print(f"  {result['message']}")
            
            # Ask if user wants to continue
            if idx < len(broker_list):
                response = input(f"\nContinue to next broker? (y/n/q to quit): ").strip().lower()
                if response == 'q':
                    print("\nStopping automation...")
                    break
                elif response == 'n':
                    print("Skipping to next...")
                    continue
        
        self.close_driver()
        self.save_results()
        self.print_summary()
    
    def save_results(self):
        """Save results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.log_dir / f"optout_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'total_processed': len(self.results),
                'results': self.results
            }, f, indent=2)
        
        print(f"\n✓ Results saved to: {results_file}")
    
    def print_summary(self):
        """Print summary of results"""
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        success = len([r for r in self.results if r['status'] == 'success'])
        manual = len([r for r in self.results if r['status'] == 'manual'])
        errors = len([r for r in self.results if r['status'] == 'error'])
        skipped = len([r for r in self.results if r['status'] == 'skipped'])
        
        print(f"\nTotal Processed: {len(self.results)}")
        print(f"✓ Successful: {success}")
        print(f"⚠ Manual Required: {manual}")
        print(f"✗ Errors: {errors}")
        print(f"○ Skipped: {skipped}")
        
        if manual > 0:
            print("\nBrokers requiring manual follow-up:")
            for r in self.results:
                if r['status'] == 'manual':
                    print(f"  - {r['broker']}")
        
        if errors > 0:
            print("\nBrokers with errors:")
            for r in self.results:
                if r['status'] == 'error':
                    print(f"  - {r['broker']}: {r['message']}")
        
        print("\n" + "="*80)
        print(f"\nScreenshots saved in: {self.log_dir}")
        print("="*80 + "\n")

def main():
    print("="*80)
    print("AUTOMATED DATA BROKER OPT-OUT TOOL")
    print("="*80)
    print("\nThis tool will help automate the opt-out process.")
    print("⚠️  Important notes:")
    print("  - Most sites still require some manual interaction")
    print("  - You may need to complete CAPTCHAs")
    print("  - Screenshots will be saved for your records")
    print("  - The browser will open and navigate to each site")
    print("\n" + "="*80 + "\n")
    
    # Get user information
    name = input("Enter your full name: ").strip()
    email = input("Enter your email address: ").strip()
    
    print("\nOptional information (press Enter to skip):")
    address = input("Address: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    zip_code = input("ZIP Code: ").strip()
    phone = input("Phone number: ").strip()
    
    user_info = {
        'name': name,
        'email': email,
        'address': address,
        'city': city,
        'state': state,
        'zip_code': zip_code,
        'phone': phone
    }
    
    # Ask if headless
    headless_choice = input("\nRun in headless mode (browser hidden)? (y/n): ").strip().lower()
    headless = headless_choice == 'y'
    
    # Confirm
    print("\nReady to start automated opt-out process.")
    confirm = input("Continue? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Cancelled.")
        return
    
    # Run automation
    tool = AutoOptOutTool(headless=headless)
    tool.run_automated_optout(user_info)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        sys.exit(0)
