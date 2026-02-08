#!/usr/bin/env python3
"""
Website Monitoring and Auto-Improvement System
Runs every 10 minutes to check website quality and make improvements.
"""

import os
import json
import time
import subprocess
import sys
from datetime import datetime
import hashlib

class WebsiteMonitor:
    def __init__(self):
        self.website_dir = os.path.dirname(os.path.abspath(__file__))
        self.status_file = "website_monitor_status.json"
        self.log_file = "website_monitor_log.txt"
        self.issues_found = 0
        self.improvements_made = 0
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        print(log_entry)
        
        # Write to log file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def load_status(self):
        """Load monitoring status from file."""
        try:
            with open(self.status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Initial status
            return {
                "last_check": None,
                "total_checks": 0,
                "total_improvements": 0,
                "last_improvement": None,
                "known_issues": {},
                "image_hashes": {}
            }
    
    def save_status(self, status):
        """Save monitoring status to file."""
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
    
    def check_main_page(self):
        """Check main index.html for issues."""
        self.log("Checking main page...")
        
        main_page = os.path.join(self.website_dir, "index.html")
        
        if not os.path.exists(main_page):
            self.log("❌ Main page not found!", "ERROR")
            return False
        
        with open(main_page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check for broken image links
        if 'src="' not in content and 'url(' not in content:
            issues.append("No image references found")
        
        # Check for city cards (should have 12)
        city_count = content.count('city-name')
        if city_count != 12:
            issues.append(f"Expected 12 city cards, found {city_count}")
        
        # Check for CSS links
        if 'bootstrap' not in content.lower():
            issues.append("Bootstrap CSS might be missing")
        
        if issues:
            self.log(f"Found {len(issues)} issues in main page", "WARNING")
            for issue in issues:
                self.log(f"  • {issue}", "WARNING")
            self.issues_found += len(issues)
        
        return len(issues) == 0
    
    def check_city_pages(self):
        """Check all city pages for issues."""
        self.log("Checking city pages...")
        
        cities_dir = os.path.join(self.website_dir, "cities")
        if not os.path.exists(cities_dir):
            self.log("❌ Cities directory not found!", "ERROR")
            return False
        
        city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html')]
        
        if len(city_files) != 12:
            self.log(f"❌ Expected 12 city pages, found {len(city_files)}", "ERROR")
            self.issues_found += 1
            return False
        
        issues = []
        for city_file in city_files:
            file_path = os.path.join(cities_dir, city_file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for hero image
            if '--hero-image:' not in content:
                issues.append(f"{city_file}: No hero image CSS variable")
            
            # Check for gallery images
            if '<img' not in content:
                issues.append(f"{city_file}: No gallery images found")
            
            # Check for back to home link
            if '../index.html' not in content:
                issues.append(f"{city_file}: Missing back to home link")
        
        if issues:
            self.log(f"Found {len(issues)} issues in city pages", "WARNING")
            for issue in issues[:3]:  # Show first 3 issues
                self.log(f"  • {issue}", "WARNING")
            if len(issues) > 3:
                self.log(f"  ... and {len(issues)-3} more issues", "WARNING")
            self.issues_found += len(issues)
        
        return len(issues) == 0
    
    def check_images(self):
        """Check image quality and consistency."""
        self.log("Checking images...")
        
        # This would check image sizes, formats, etc.
        # For now, just check if update scripts exist
        scripts = [
            "update_city_images_v2.py",
            "update_city_page_images.py",
            "fix_city_page_images.py"
        ]
        
        missing_scripts = []
        for script in scripts:
            if not os.path.exists(os.path.join(self.website_dir, script)):
                missing_scripts.append(script)
        
        if missing_scripts:
            self.log(f"Missing {len(missing_scripts)} image update scripts", "WARNING")
            for script in missing_scripts:
                self.log(f"  • {script}", "WARNING")
            self.issues_found += len(missing_scripts)
        
        return len(missing_scripts) == 0
    
    def run_improvements(self):
        """Run improvement scripts based on detected issues."""
        self.log("Running improvement scripts...")
        
        improvements = []
        
        # Always run image updates to ensure consistency
        try:
            self.log("Running image consistency check...")
            result = subprocess.run(
                [sys.executable, "verify_images.py"],
                cwd=self.website_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                if "✅" in result.stdout or "SUCCESS" in result.stdout:
                    self.log("✅ Image verification passed")
                else:
                    self.log("⚠️ Image verification found issues", "WARNING")
                    # Run fix script
                    self.log("Running image fix script...")
                    subprocess.run(
                        [sys.executable, "fix_city_page_images.py"],
                        cwd=self.website_dir,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    improvements.append("Fixed image inconsistencies")
                    self.improvements_made += 1
            else:
                self.log("❌ Image verification failed", "ERROR")
                
        except Exception as e:
            self.log(f"❌ Error running improvements: {e}", "ERROR")
        
        # Check for missing city pages and create them
        cities_dir = os.path.join(self.website_dir, "cities")
        city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html')] if os.path.exists(cities_dir) else []
        
        if len(city_files) < 12:
            self.log(f"Only {len(city_files)} city pages found, creating missing ones...")
            try:
                subprocess.run(
                    [sys.executable, "create_missing_city_pages.py"],
                    cwd=self.website_dir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                improvements.append(f"Created {12 - len(city_files)} missing city pages")
                self.improvements_made += 1
            except Exception as e:
                self.log(f"❌ Error creating city pages: {e}", "ERROR")
        
        return improvements
    
    def run_check(self):
        """Run one complete check cycle."""
        self.log("\n" + "=" * 60)
        self.log("WEBSITE MONITOR - STARTING CHECK")
        self.log("=" * 60)
        
        # Load previous status
        status = self.load_status()
        status["total_checks"] = status.get("total_checks", 0) + 1
        status["last_check"] = datetime.now().isoformat()
        
        # Reset counters
        self.issues_found = 0
        self.improvements_made = 0
        
        # Run checks
        checks = [
            ("Main Page", self.check_main_page),
            ("City Pages", self.check_city_pages),
            ("Images", self.check_images)
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            try:
                if check_func():
                    self.log(f"✅ {check_name}: PASSED")
                else:
                    self.log(f"⚠️ {check_name}: FAILED", "WARNING")
                    all_passed = False
            except Exception as e:
                self.log(f"❌ {check_name}: ERROR - {e}", "ERROR")
                all_passed = False
        
        # Run improvements
        improvements = self.run_improvements()
        
        # Update status
        if improvements:
            status["total_improvements"] = status.get("total_improvements", 0) + self.improvements_made
            status["last_improvement"] = datetime.now().isoformat()
        
        self.save_status(status)
        
        # Summary
        self.log("\n" + "=" * 60)
        self.log("CHECK SUMMARY")
        self.log("=" * 60)
        self.log(f"Issues found: {self.issues_found}")
        self.log(f"Improvements made: {self.improvements_made}")
        
        if improvements:
            self.log("\nImprovements applied:")
            for improvement in improvements:
                self.log(f"  • {improvement}")
        
        self.log(f"\nTotal checks run: {status['total_checks']}")
        self.log(f"Total improvements: {status['total_improvements']}")
        
        if all_passed and self.issues_found == 0:
            self.log("\n🎉 WEBSITE STATUS: EXCELLENT")
        elif self.improvements_made > 0:
            self.log("\n🔧 WEBSITE STATUS: IMPROVED")
        else:
            self.log("\n⚠️ WEBSITE STATUS: NEEDS ATTENTION")
        
        self.log("=" * 60)
        
        return all_passed

def main():
    """Main function for manual run."""
    monitor = WebsiteMonitor()
    monitor.run_check()

if __name__ == "__main__":
    main()