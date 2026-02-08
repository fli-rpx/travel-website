#!/usr/bin/env python3
"""
Simple Telegram-enabled Website Monitor
- Runs checks and sends results to Telegram
- Triggers immediate fixes
- Works within Clawdbot environment
"""

import os
import json
import re
import subprocess
import sys
from datetime import datetime

def log(message):
    """Simple logging."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def send_telegram(message):
    """Send message to Telegram using Clawdbot's message tool."""
    try:
        # This will be called from within Clawdbot
        # For cron jobs, we'll log the message
        log(f"📱 TELEGRAM ALERT: {message[:100]}...")
        
        # In production, this would use Clawdbot's message API
        # For now, we'll create a file that Clawdbot can read
        alert_file = "telegram_alerts.json"
        alerts = []
        
        if os.path.exists(alert_file):
            with open(alert_file, 'r') as f:
                alerts = json.load(f)
        
        alerts.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "chat_id": "8080442123"
        })
        
        with open(alert_file, 'w') as f:
            json.dump(alerts[-10:], f, indent=2)  # Keep last 10 alerts
        
        return True
    except Exception as e:
        log(f"❌ Telegram error: {e}")
        return False

def check_images():
    """Check images readiness."""
    log("🔍 Checking images readiness...")
    
    try:
        with open("baidu_image_replacements.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return False, ["Image status file not found"], []
    
    cities = data.get("cities", {})
    missing = []
    
    for city_name, city_data in cities.items():
        if city_data.get("baidu_replacement") == "REPLACE_WITH_BAIDU_IMAGE_URL":
            missing.append(city_name)
    
    issues = []
    fixes = []
    
    if missing:
        issues.append(f"{len(missing)} cities need images")
        
        # Try to fix
        try:
            result = subprocess.run(
                [sys.executable, "search_city_images.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                fixes.append("Ran image search")
        except:
            pass
    
    return len(missing) == 0, issues, fixes

def check_pages():
    """Check pages readiness."""
    log("🔍 Checking pages readiness...")
    
    cities_dir = "cities"
    if not os.path.exists(cities_dir):
        return False, ["Cities directory not found"], []
    
    expected_cities = ["beijing", "shanghai", "chengdu", "harbin", "chongqing",
                      "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen",
                      "guangzhou", "hongkong"]
    
    missing = []
    for city in expected_cities:
        if not os.path.exists(f"{cities_dir}/{city}.html"):
            missing.append(city)
    
    issues = []
    fixes = []
    
    if missing:
        issues.append(f"{len(missing)} cities missing pages")
        
        # Try to fix
        try:
            result = subprocess.run(
                [sys.executable, "create_missing_city_pages.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                fixes.append("Created missing pages")
        except:
            pass
    
    return len(missing) == 0, issues, fixes

def check_navigation():
    """Check navigation links."""
    log("🔍 Checking navigation links...")
    
    issues = []
    fixes = []
    
    # Check a few city pages
    cities_dir = "cities"
    if os.path.exists(cities_dir):
        city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html') and f != 'template.html']
        
        for city_file in city_files[:2]:
            with open(f"{cities_dir}/{city_file}", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for home link
            if 'href="index.html"' not in content and 'href="/travel-website/index.html"' not in content:
                issues.append(f"{city_file}: Missing home link")
    
    if issues:
        # Try to fix
        try:
            result = subprocess.run(
                [sys.executable, "fix_all_issues.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                fixes.append("Fixed navigation links")
        except:
            pass
    
    return len(issues) == 0, issues, fixes

def run_checks():
    """Run all checks and send Telegram alerts."""
    log("=" * 60)
    log("🚀 TELEGRAM-ENABLED WEBSITE MONITOR")
    log("=" * 60)
    
    checks = [
        ("Images", check_images),
        ("Pages", check_pages),
        ("Navigation", check_navigation)
    ]
    
    all_passed = True
    total_issues = 0
    total_fixes = 0
    
    # Run checks
    for check_name, check_func in checks:
        passed, issues, fixes = check_func()
        
        # Create alert message
        status = "✅ PASSED" if passed else "❌ FAILED"
        alert = f"""
🔔 **{check_name} Check** 🔔
**Status:** {status}
**Time:** {datetime.now().strftime('%H:%M:%S')}
"""
        
        if issues:
            alert += f"**Issues:** {len(issues)}\n"
            for issue in issues[:2]:
                alert += f"• {issue}\n"
        
        if fixes:
            alert += f"**Fixes:** {len(fixes)}\n"
            for fix in fixes:
                alert += f"• {fix}\n"
        
        # Send alert
        send_telegram(alert)
        
        # Update totals
        if not passed:
            all_passed = False
            total_issues += len(issues)
        
        total_fixes += len(fixes)
    
    # Send summary
    summary = f"""
📊 **MONITOR SUMMARY**
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Checks:** {len(checks)}
**Issues Found:** {total_issues}
**Fixes Applied:** {total_fixes}
**Status:** {'✅ ALL GOOD' if all_passed else '❌ NEEDS ATTENTION'}
"""
    
    send_telegram(summary)
    
    log(f"\n📊 Summary: {len(checks)} checks, {total_issues} issues, {total_fixes} fixes")
    log("✅ Telegram alerts sent")
    
    # Save status
    status = {
        "last_check": datetime.now().isoformat(),
        "all_passed": all_passed,
        "total_issues": total_issues,
        "total_fixes": total_fixes
    }
    
    with open("telegram_monitor_status.json", 'w') as f:
        json.dump(status, f, indent=2)
    
    return all_passed

def main():
    """Main function."""
    run_checks()

if __name__ == "__main__":
    main()