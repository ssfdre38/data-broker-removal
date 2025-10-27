#!/usr/bin/env python3
"""
Data Broker Removal Request Generator
Generates removal request emails and provides opt-out links for major data brokers.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

class DataBrokerRemovalTool:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.data_file = self.script_dir / "data_brokers.json"
        self.output_dir = self.script_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.brokers = self.load_brokers()
        
    def load_brokers(self):
        """Load data broker information from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.data_file} not found")
            sys.exit(1)
            
    def generate_email_template(self, name, email, address="", phone="", city="", state="", zip_code=""):
        """Generate a CCPA/GDPR compliant removal request email"""
        template = f"""Subject: Data Removal Request - {name}

Dear Privacy Team,

I am writing to request the removal of my personal information from your database under the California Consumer Privacy Act (CCPA), General Data Protection Regulation (GDPR), and other applicable privacy laws.

Personal Information to Remove:
Name: {name}
Email: {email}
"""
        
        if address:
            template += f"Address: {address}\n"
        if city:
            template += f"City: {city}\n"
        if state:
            template += f"State: {state}\n"
        if zip_code:
            template += f"ZIP Code: {zip_code}\n"
        if phone:
            template += f"Phone: {phone}\n"
            
        template += """
I formally request that you:
1. Remove all of my personal information from your database
2. Stop selling or sharing my personal information with third parties
3. Confirm in writing once my information has been removed
4. Do not retaliate or discriminate against me for making this request

Please process this request within 45 days as required by law. I expect written confirmation of the removal.

Thank you for your prompt attention to this matter.

Sincerely,
"""
        template += f"{name}\n"
        template += f"Date: {datetime.now().strftime('%B %d, %Y')}\n"
        
        return template
    
    def generate_removal_list(self, name, email, address="", phone="", city="", state="", zip_code=""):
        """Generate a comprehensive removal list with instructions"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate email template
        email_template = self.generate_email_template(name, email, address, phone, city, state, zip_code)
        email_file = self.output_dir / f"email_template_{timestamp}.txt"
        with open(email_file, 'w') as f:
            f.write(email_template)
        
        # Generate removal checklist
        checklist_file = self.output_dir / f"removal_checklist_{timestamp}.html"
        html_content = self.generate_html_checklist(name, email, address, phone, city, state, zip_code)
        with open(checklist_file, 'w') as f:
            f.write(html_content)
        
        # Generate text checklist
        text_checklist = self.output_dir / f"removal_checklist_{timestamp}.txt"
        with open(text_checklist, 'w') as f:
            f.write(f"DATA BROKER REMOVAL CHECKLIST\n")
            f.write(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"Personal Information:\n")
            f.write(f"  Name: {name}\n")
            f.write(f"  Email: {email}\n")
            if address:
                f.write(f"  Address: {address}\n")
            if city:
                f.write(f"  City: {city}\n")
            if state:
                f.write(f"  State: {state}\n")
            if zip_code:
                f.write(f"  ZIP: {zip_code}\n")
            if phone:
                f.write(f"  Phone: {phone}\n")
            f.write(f"\n{'='*80}\n\n")
            
            for idx, broker in enumerate(self.brokers, 1):
                f.write(f"{idx}. {broker['name']}\n")
                f.write(f"   Website: {broker['website']}\n")
                f.write(f"   Opt-Out URL: {broker['opt_out_url']}\n")
                f.write(f"   Method: {broker['method']}\n")
                if broker.get('email'):
                    f.write(f"   Email: {broker['email']}\n")
                f.write(f"   Status: [ ] Pending  [ ] Completed  [ ] N/A\n")
                f.write(f"   Date Submitted: _______________\n")
                f.write(f"   Confirmation Received: _______________\n")
                f.write(f"\n{'-'*80}\n\n")
        
        return {
            'email_template': str(email_file),
            'html_checklist': str(checklist_file),
            'text_checklist': str(text_checklist)
        }
    
    def generate_html_checklist(self, name, email, address="", phone="", city="", state="", zip_code=""):
        """Generate an interactive HTML checklist"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Broker Removal Checklist</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .info-box {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .broker-card {
            background-color: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: relative;
        }
        .broker-card.completed {
            background-color: #d4edda;
            border-left: 4px solid #28a745;
        }
        .broker-name {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .broker-info {
            margin: 5px 0;
            color: #555;
        }
        .opt-out-button {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 5px 0 0;
        }
        .opt-out-button:hover {
            background-color: #2980b9;
        }
        .checkbox-container {
            position: absolute;
            top: 20px;
            right: 20px;
        }
        .checkbox-container input[type="checkbox"] {
            width: 25px;
            height: 25px;
            cursor: pointer;
        }
        .progress-bar {
            width: 100%;
            height: 30px;
            background-color: #ecf0f1;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 10px;
        }
        .progress-fill {
            height: 100%;
            background-color: #27ae60;
            width: 0%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .instructions {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .method-badge {
            display: inline-block;
            padding: 5px 10px;
            background-color: #6c757d;
            color: white;
            border-radius: 3px;
            font-size: 12px;
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 Data Broker Removal Checklist</h1>
        <p>Generated: """ + datetime.now().strftime('%B %d, %Y at %I:%M %p') + """</p>
    </div>
    
    <div class="info-box">
        <h3>Your Information</h3>
        <p><strong>Name:</strong> """ + name + """</p>
        <p><strong>Email:</strong> """ + email + """</p>"""
        
        if address:
            html += f"<p><strong>Address:</strong> {address}</p>"
        if city:
            html += f"<p><strong>City:</strong> {city}</p>"
        if state:
            html += f"<p><strong>State:</strong> {state}</p>"
        if zip_code:
            html += f"<p><strong>ZIP:</strong> {zip_code}</p>"
        if phone:
            html += f"<p><strong>Phone:</strong> {phone}</p>"
            
        html += """
        <div class="progress-bar">
            <div class="progress-fill" id="progressBar">0%</div>
        </div>
    </div>
    
    <div class="instructions">
        <h3>📋 Instructions</h3>
        <ol>
            <li>Click "Visit Opt-Out Page" for each data broker</li>
            <li>Follow their removal process (usually requires searching for yourself first)</li>
            <li>Check the box when you've submitted your removal request</li>
            <li>Keep track of confirmation emails</li>
            <li>Follow up after 45 days if you haven't received confirmation</li>
        </ol>
        <p><strong>Tip:</strong> Some sites require you to find your listing first before you can opt out. Search for your name, address, or phone number.</p>
    </div>
    
    <div id="brokerList">
"""
        
        for idx, broker in enumerate(self.brokers, 1):
            html += f"""
        <div class="broker-card" id="broker-{idx}">
            <div class="checkbox-container">
                <input type="checkbox" id="check-{idx}" onchange="updateProgress()">
            </div>
            <div class="broker-name">{idx}. {broker['name']}</div>
            <div class="broker-info">🌐 <a href="{broker['website']}" target="_blank">{broker['website']}</a></div>
            <div class="broker-info">
                <span class="method-badge">{broker['method'].replace('_', ' ').upper()}</span>
"""
            if broker.get('email'):
                html += f'<span class="method-badge">EMAIL: {broker["email"]}</span>'
            
            html += f"""
            </div>
            <a href="{broker['opt_out_url']}" target="_blank" class="opt-out-button">Visit Opt-Out Page →</a>
        </div>
"""
        
        html += """
    </div>
    
    <script>
        function updateProgress() {
            const total = """ + str(len(self.brokers)) + """;
            const checked = document.querySelectorAll('input[type="checkbox"]:checked').length;
            const percentage = Math.round((checked / total) * 100);
            const progressBar = document.getElementById('progressBar');
            progressBar.style.width = percentage + '%';
            progressBar.textContent = percentage + '%';
            
            // Update card appearance
            for (let i = 1; i <= total; i++) {
                const checkbox = document.getElementById('check-' + i);
                const card = document.getElementById('broker-' + i);
                if (checkbox.checked) {
                    card.classList.add('completed');
                } else {
                    card.classList.remove('completed');
                }
            }
            
            // Save progress to localStorage
            const progress = [];
            for (let i = 1; i <= total; i++) {
                progress.push(document.getElementById('check-' + i).checked);
            }
            localStorage.setItem('brokerProgress', JSON.stringify(progress));
        }
        
        // Load saved progress
        window.onload = function() {
            const saved = localStorage.getItem('brokerProgress');
            if (saved) {
                const progress = JSON.parse(saved);
                progress.forEach((checked, index) => {
                    const checkbox = document.getElementById('check-' + (index + 1));
                    if (checkbox) {
                        checkbox.checked = checked;
                    }
                });
                updateProgress();
            }
        };
    </script>
</body>
</html>
"""
        return html
    
    def list_brokers(self):
        """List all data brokers"""
        print(f"\nTotal Data Brokers: {len(self.brokers)}\n")
        print("="*80)
        for idx, broker in enumerate(self.brokers, 1):
            print(f"\n{idx}. {broker['name']}")
            print(f"   Website: {broker['website']}")
            print(f"   Opt-Out: {broker['opt_out_url']}")
            if broker.get('email'):
                print(f"   Email: {broker['email']}")
        print("\n" + "="*80)

def main():
    tool = DataBrokerRemovalTool()
    
    print("="*80)
    print("DATA BROKER REMOVAL REQUEST GENERATOR")
    print("="*80)
    print("\nThis tool helps you send removal requests to major data brokers.")
    print(f"Found {len(tool.brokers)} data brokers in database.\n")
    
    # Get user information
    name = input("Enter your full name: ").strip()
    email = input("Enter your email address: ").strip()
    
    print("\nOptional information (press Enter to skip):")
    address = input("Address: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    zip_code = input("ZIP Code: ").strip()
    phone = input("Phone number: ").strip()
    
    print("\nGenerating removal requests...")
    
    files = tool.generate_removal_list(name, email, address, phone, city, state, zip_code)
    
    print("\n" + "="*80)
    print("✅ GENERATION COMPLETE!")
    print("="*80)
    print(f"\nGenerated files:")
    print(f"1. Email Template: {files['email_template']}")
    print(f"2. HTML Checklist: {files['html_checklist']}")
    print(f"3. Text Checklist: {files['text_checklist']}")
    
    print(f"\n📧 Email Template:")
    print("   Use this template when sending emails to data brokers")
    
    print(f"\n🌐 HTML Checklist:")
    print("   Open this in your browser to track your progress")
    print("   Each broker has a clickable link to their opt-out page")
    print("   Check off each one as you complete them")
    
    print(f"\n📝 Text Checklist:")
    print("   Printable version for offline tracking")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Open the HTML checklist in your browser")
    print("2. Visit each opt-out link and follow their process")
    print("3. Most sites require you to search for yourself first")
    print("4. Check the box after submitting each request")
    print("5. Keep track of confirmation emails")
    print("6. Follow up after 45 days if no response")
    print("\n⚠️  Note: Some brokers may require photo ID verification")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
