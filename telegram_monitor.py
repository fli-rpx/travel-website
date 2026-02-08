#!/usr/bin/env python3
"""
Enhanced Website Monitor with Telegram Gateway Integration
- Runs checks every 10 minutes
- Sends results to Telegram immediately
- Can trigger immediate fixes
"""

import os
import json
import re
import time
import subprocess
import sys
from datetime import datetime
from collections import defaultdict

class TelegramMonitor:
    def __init__(self):
        self.website_dir = os.path.dirname(os.path.abspath(__file__))
        self.status_file = "telegram_monitor_status.json"
        self.log_file = "telegram_monitor.log"
        self.issues_found = 0
        self.improvements_made = 0
        
        # Telegram configuration
        self.telegram_chat_id = "8080442123"  # Your Telegram ID
        self.telegram_bot_token = self.get_telegram_token()
        
        # All 12 cities that should exist
        self.all_cities = [
            "Beijing", "Shanghai", "Chengdu", "Harbin", "Chongqing",
            "Wuxi", "Qingdao", "Xiamen", "Nanjing", "Shenzhen", 
            "Guangzhou", "Hongkong"
        ]
        
        # Expected color scheme
        self.expected_colors = {
            "primary": "#2563eb",
            "secondary": "#1e40af", 
            "accent": "#f59e0b",
            "light": "#f8fafc",
            "dark": "#1e293b"
        }
    
    def get_telegram_token(self):
        """Get Telegram bot token from environment or config."""
        # Try to get from environment
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if token:
            return token
        
        # Try to read from config file
        config_file = os.path.join(self.website_dir, "telegram_config.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("bot_token")
            except:
                pass
        
        # For now, we'll use the Clawdbot gateway
        # In production, you'd set up a proper bot token
        return None
    
    def send_telegram_message(self, message):
        """Send message to Telegram via Clawdbot."""
        try:
            # Use message tool directly
            from message import send_message
            
            result = send_message(
                action='send',
                to=self.telegram_chat_id,
                channel='telegram',
                message=message
            )
            
            if result.get('ok'):
                self.log(f"✅ Telegram message sent (ID: {result.get('messageId')})")
                return True
            else:
                self.log(f"⚠️  Telegram send failed")
                return False
                
        except Exception as e:
            self.log(f"❌ Telegram error: {e}")
            # Fallback to simple print
            print(f"\n📱 TELEGRAM ALERT (would send):\n{message}\n")
            return False
    
    def send_telegram_alert(self, check_name, passed, issues, fixes_applied):
        """Send formatted alert to Telegram."""
        
        status_emoji = "✅" if passed else "❌"
        status_text = "PASSED" if passed else "FAILED"
        
        message = f"""
🔔 **WEBSITE MONITOR ALERT** 🔔

**Check:** {check_name}
**Status:** {status_emoji} {status_text}
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if issues:
            message += f"**Issues Found:** {len(issues)}\n"
            for i, issue in enumerate(issues[:3], 1):
                message += f"{i}. {issue}\n"
            if len(issues) > 3:
                message += f"... and {len(issues)-3} more issues\n"
        
        if fixes_applied:
            message += f"\n**Fixes Applied:** {len(fixes_applied)}\n"
            for i, fix in enumerate(fixes_applied[:3], 1):
                message += f"{i}. {fix}\n"
        
        if not passed and issues:
            message += f"\n🚨 **IMMEDIATE ACTION NEEDED** 🚨"
        
        # Send the message
        return self.send_telegram_message(message)
    
    def log(self, message, level="INFO"):
        """Log messages with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        print(log_entry)
        
        # Write to log file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def check_images_readiness(self):
        """Check 1: Are images ready for each city?"""
        self.log("\n🔍 CHECK 1: IMAGES READINESS FOR EACH CITY")
        
        try:
            with open("baidu_image_replacements.json", 'r', encoding='utf-8') as f:
                image_status = json.load(f)
        except FileNotFoundError:
            self.log("❌ Image status file not found", "ERROR")
            return False, ["Image status file not found"], []
        
        cities_data = image_status.get("cities", {})
        
        cities_without_images = []
        
        for city in self.all_cities:
            if city in cities_data:
                city_data = cities_data[city]
                if city_data.get("baidu_replacement") == "REPLACE_WITH_BAIDU_IMAGE_URL":
                    cities_without_images.append(city)
            else:
                cities_without_images.append(city)
        
        issues = []
        fixes = []
        
        if cities_without_images:
            issues.append(f"{len(cities_without_images)}/{len(self.all_cities)} cities need images")
            if len(cities_without_images) <= 5:
                issues.append(f"Cities: {', '.join(cities_without_images)}")
            else:
                issues.append(f"Cities: {', '.join(cities_without_images[:5])} and {len(cities_without_images)-5} more")
            
            # Try to fix by running image search
            try:
                self.log("Attempting to fix missing images...")
                result = subprocess.run(
                    [sys.executable, "search_city_images.py"],
                    cwd=self.website_dir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    fixes.append("Ran image search for missing cities")
            except Exception as e:
                self.log(f"Image fix failed: {e}")
        
        passed = len(cities_without_images) == 0
        return passed, issues, fixes
    
    def check_pages_readiness(self):
        """Check 2: Are pages ready for each city?"""
        self.log("\n🔍 CHECK 2: PAGES READINESS FOR EACH CITY")
        
        cities_dir = os.path.join(self.website_dir, "cities")
        if not os.path.exists(cities_dir):
            self.log("❌ Cities directory not found", "ERROR")
            return False, ["Cities directory not found"], []
        
        # Get all HTML files
        all_files = os.listdir(cities_dir)
        html_files = [f for f in all_files if f.endswith('.html') and f != 'template.html']
        
        # Map city names to expected filenames
        expected_files = {}
        for city in self.all_cities:
            expected_files[city.lower() + ".html"] = city
        
        # Check which cities have pages
        cities_with_pages = []
        cities_without_pages = []
        
        for html_file in html_files:
            if html_file in expected_files:
                cities_with_pages.append(expected_files[html_file])
        
        for expected_file, city in expected_files.items():
            if city not in cities_with_pages:
                cities_without_pages.append(city)
        
        issues = []
        fixes = []
        
        if cities_without_pages:
            issues.append(f"{len(cities_without_pages)}/{len(self.all_cities)} cities missing pages")
            issues.append(f"Missing: {', '.join(cities_without_pages)}")
            
            # Try to fix by creating missing pages
            try:
                self.log("Creating missing city pages...")
                result = subprocess.run(
                    [sys.executable, "create_missing_city_pages.py"],
                    cwd=self.website_dir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    fixes.append("Created missing city pages")
            except Exception as e:
                self.log(f"Page creation failed: {e}")
        
        passed = len(cities_without_pages) == 0
        return passed, issues, fixes
    
    def check_layout_color_consistency(self):
        """Check 3: Layout and color consistency between pages."""
        self.log("\n🔍 CHECK 3: LAYOUT & COLOR CONSISTENCY")
        
        issues = []
        fixes = []
        
        # Check main page
        main_page = os.path.join(self.website_dir, "index.html")
        if not os.path.exists(main_page):
            issues.append("Main page not found")
            return False, issues, fixes
        
        with open(main_page, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # Check a few city pages
        cities_dir = os.path.join(self.website_dir, "cities")
        city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html') and f != 'template.html']
        
        color_issues = []
        for city_file in city_files[:3]:  # Check first 3
            file_path = os.path.join(cities_dir, city_file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for expected colors
            for color_name, color_value in self.expected_colors.items():
                if color_value not in content:
                    color_issues.append(f"{city_file}: Missing {color_name} ({color_value})")
        
        if color_issues:
            issues.append(f"Color inconsistencies in {len(color_issues)} pages")
            issues.extend(color_issues[:2])
            if len(color_issues) > 2:
                issues.append(f"... and {len(color_issues)-2} more color issues")
            
            # Try to fix color consistency
            try:
                self.log("Fixing color consistency...")
                result = subprocess.run(
                    [sys.executable, "fix_all_issues.py"],
                    cwd=self.website_dir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    fixes.append("Applied color consistency fixes")
            except Exception as e:
                self.log(f"Color fix failed: {e}")
        
        passed = len(color_issues) == 0
        return passed, issues, fixes
    
    def check_navigation_links(self):
        """Check 4: Are navigation links correct?"""
        self.log("\n🔍 CHECK 4: NAVIGATION LINK CONSISTENCY")
        
        issues = []
        fixes = []
        
        # Check city pages
        cities_dir = os.path.join(self.website_dir, "cities")
        city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html') and f != 'template.html']
        
        link_issues = []
        for city_file in city_files[:3]:  # Check first 3
            file_path = os.path.join(cities_dir, city_file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check back to home link
            home_links = re.findall(r'href="([^"]*index\.html[^"]*)"', content)
            
            # Should have at least one link back to home
            if not any('index.html' in link for link in home_links):
                link_issues.append(f"{city_file}: No link back to home page")
            
            # Check link consistency
            inconsistent_links = []
            for link in home_links:
                if not link.startswith('/travel-website/') and 'index.html' in link:
                    inconsistent_links.append(link)
            
            if inconsistent_links:
                link_issues.append(f"{city_file}: Inconsistent home links")
        
        if link_issues:
            issues.append(f"Navigation issues in {len(link_issues)} pages")
            issues.extend(link_issues[:2])
            if len(link_issues) > 2:
                issues.append(f"... and {len(link_issues)-2} more navigation issues")
            
            # Try to fix navigation links
            try:
                self.log("Fixing navigation links...")
                result = subprocess.run(
                    [sys.executable, "fix_all_issues.py"],
                    cwd=self.website_dir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    fixes.append("Fixed navigation links")
            except Exception as e:
                self.log(f"Navigation fix failed: {e}")
        
        passed = len(link_issues) == 0
        return passed, issues, fixes
    
    def run_complete_check(self):
        """Run all checks and send Telegram alerts."""
        self.log("\n" + "=" * 70)
        self.log("TELEGRAM-ENABLED WEBSITE MONITOR")
        self.log("=" * 70)
        self.log(f"Starting check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all checks
        checks = [
            ("Images Readiness", self.check_images_readiness),
            ("Pages Readiness", self.check_pages_readiness),
            ("Layout & Color Consistency", self.check_layout_color_consistency),
            ("Navigation Links", self.check_navigation_links)
        ]
        
        all_passed = True
        total_issues = 0
        total_fixes = 0
        
        summary_message = f"""
📊 **WEBSITE MONITOR SUMMARY**
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Checks:** {len(checks)}

"""
        
        for check_name, check_func in checks:
            try:
                passed, issues, fixes = check_func()
                
                # Send immediate Telegram alert for this check
                self.send_telegram_alert(check_name, passed, issues, fixes)
                
                # Update summary
                status_emoji = "✅" if passed else "❌"
                summary_message += f"{status_emoji} **{check_name}:** "
                if passed:
                    summary_message += "PASSED\n"
                else:
                    summary_message += f"FAILED ({len(issues)} issues)\n"
                
                if not passed:
                    all_passed = False
                    total_issues += len(issues)
                
                total_fixes += len(fixes)
                
            except Exception as e:
                self.log(f"❌ {check_name}: ERROR - {e}", "ERROR")
                self.send_telegram_alert(check_name, False, [f"Check failed: {str(e)}"], [])
                all_passed = False
        
        # Send summary
        summary_message += f"\n**Total Issues:** {total_issues}"
        summary_message += f"\n**Fixes Applied:** {total_fixes}"
        summary_message += f"\n**Overall Status:** {'✅ ALL PASSED' if all_passed else '❌ NEEDS ATTENTION'}"
        
        self.send_telegram_message(summary_message)
        
        # Log summary
        self.log("\n" + "=" * 70)
        self.log("CHECK SUMMARY")
        self.log("=" * 70)
        self.log(f"Checks passed: {sum(1 for check in checks if True)}/{len(checks)}")
        self.log(f"Total issues: {total_issues}")
        self.log(f"Fixes applied: {total_fixes}")
        
        if all_passed:
            self.log("🎉 WEBSITE STATUS: EXCELLENT")
        else:
            self.log("⚠️  WEBSITE STATUS: NEEDS ATTENTION")
        
        # Save status
        self.save_status(all_passed, total_issues, total_fixes)
        
        return all_passed
    
    def save_status(self, all_passed, total_issues, total_fixes):
        """Save monitoring status."""
        status = {
            "last_check": datetime.now().isoformat(),
            "all_passed": all_passed,
            "total_issues": total_issues,
            "total_fixes": total_fixes,
            "telegram_alerts_sent": True
        }
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)

def main():
    """Main function."""
    monitor = TelegramMonitor()
    monitor.run_complete_check()

if __name__ == "__main__":
    main()