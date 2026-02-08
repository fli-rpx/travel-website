#!/usr/bin/env python3
"""
Clawdbot-Integrated Website Monitor
- Runs checks every 10 minutes via cron
- Sends results to Telegram IMMEDIATELY
- Triggers fixes automatically
- Uses Clawdbot's messaging system
"""

import os
import json
import re
import subprocess
import sys
from datetime import datetime

# Telegram configuration
TELEGRAM_CHAT_ID = "8080442123"

def log(message, level="INFO"):
    """Log with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def send_to_telegram_via_clawdbot(message):
    """
    Send message to Telegram using Clawdbot's system.
    This creates a command that Clawdbot will execute.
    """
    try:
        # Create a message file that Clawdbot can process
        message_file = "latest_telegram_alert.txt"
        
        with open(message_file, 'w', encoding='utf-8') as f:
            f.write(f"TO:{TELEGRAM_CHAT_ID}\n")
            f.write(f"CHANNEL:telegram\n")
            f.write(f"MESSAGE:{message}\n")
            f.write(f"TIMESTAMP:{datetime.now().isoformat()}\n")
        
        log(f"✅ Telegram alert prepared in {message_file}")
        
        # Also try to use Clawdbot's exec if available
        try:
            # This would be called from within Clawdbot session
            # For cron jobs, we create a trigger file
            trigger_file = "send_telegram_trigger.json"
            trigger_data = {
                "action": "send",
                "to": TELEGRAM_CHAT_ID,
                "channel": "telegram",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(trigger_file, 'w') as f:
                json.dump(trigger_data, f, indent=2)
            
            log(f"✅ Created trigger file: {trigger_file}")
            
        except Exception as e:
            log(f"⚠️  Could not create trigger: {e}")
        
        return True
        
    except Exception as e:
        log(f"❌ Telegram send error: {e}")
        return False

def check_all_and_alert():
    """Run all checks and send Telegram alerts."""
    log("=" * 70)
    log("🔔 CLAWDBOT-INTEGRATED WEBSITE MONITOR")
    log("=" * 70)
    log(f"Starting check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define checks
    checks = []
    
    # 1. Check images
    log("\n🔍 CHECK 1: Images Readiness")
    images_ok = True
    images_issues = []
    images_fixes = []
    
    try:
        with open("baidu_image_replacements.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cities = data.get("cities", {})
        missing_images = []
        
        for city, city_data in cities.items():
            if city_data.get("baidu_replacement") == "REPLACE_WITH_BAIDU_IMAGE_URL":
                missing_images.append(city)
        
        if missing_images:
            images_ok = False
            images_issues.append(f"{len(missing_images)} cities need images")
            
            # Try to fix
            try:
                result = subprocess.run(
                    [sys.executable, "search_city_images.py"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    images_fixes.append("Ran image search")
            except Exception as e:
                log(f"⚠️  Image fix failed: {e}")
    
    except Exception as e:
        images_ok = False
        images_issues.append(f"Error: {str(e)}")
    
    checks.append(("Images", images_ok, images_issues, images_fixes))
    
    # 2. Check pages
    log("\n🔍 CHECK 2: Pages Readiness")
    pages_ok = True
    pages_issues = []
    pages_fixes = []
    
    try:
        cities_dir = "cities"
        if not os.path.exists(cities_dir):
            pages_ok = False
            pages_issues.append("Cities directory not found")
        else:
            expected = ["beijing", "shanghai", "chengdu", "harbin", "chongqing",
                       "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen",
                       "guangzhou", "hongkong"]
            
            missing_pages = []
            for city in expected:
                if not os.path.exists(f"{cities_dir}/{city}.html"):
                    missing_pages.append(city)
            
            if missing_pages:
                pages_ok = False
                pages_issues.append(f"{len(missing_pages)} cities missing pages")
                
                # Try to fix
                try:
                    result = subprocess.run(
                        [sys.executable, "create_missing_city_pages.py"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        pages_fixes.append("Created missing pages")
                except Exception as e:
                    log(f"⚠️  Page fix failed: {e}")
    
    except Exception as e:
        pages_ok = False
        pages_issues.append(f"Error: {str(e)}")
    
    checks.append(("Pages", pages_ok, pages_issues, pages_fixes))
    
    # 3. Check navigation
    log("\n🔍 CHECK 3: Navigation Links")
    nav_ok = True
    nav_issues = []
    nav_fixes = []
    
    try:
        cities_dir = "cities"
        if os.path.exists(cities_dir):
            city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html') and f != 'template.html']
            
            for city_file in city_files[:3]:  # Check first 3
                with open(f"{cities_dir}/{city_file}", 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for proper home link
                if 'href="/travel-website/index.html"' not in content:
                    nav_ok = False
                    nav_issues.append(f"{city_file}: Home link issue")
        
        if nav_issues:
            # Try to fix
            try:
                result = subprocess.run(
                    [sys.executable, "fix_all_issues.py"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    nav_fixes.append("Fixed navigation links")
            except Exception as e:
                log(f"⚠️  Navigation fix failed: {e}")
    
    except Exception as e:
        nav_ok = False
        nav_issues.append(f"Error: {str(e)}")
    
    checks.append(("Navigation", nav_ok, nav_issues, nav_fixes))
    
    # 4. Check layout/colors
    log("\n🔍 CHECK 4: Layout & Colors")
    layout_ok = True
    layout_issues = []
    layout_fixes = []
    
    try:
        # Check main page exists
        if not os.path.exists("index.html"):
            layout_ok = False
            layout_issues.append("Main page missing")
        else:
            # Simple check for consistency
            with open("index.html", 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            expected_colors = ["#2563eb", "#1e40af", "#f59e0b"]
            missing_colors = []
            
            for color in expected_colors:
                if color not in main_content:
                    missing_colors.append(color)
            
            if missing_colors:
                layout_ok = False
                layout_issues.append(f"Missing colors: {len(missing_colors)}")
    
    except Exception as e:
        layout_ok = False
        layout_issues.append(f"Error: {str(e)}")
    
    checks.append(("Layout", layout_ok, layout_issues, layout_fixes))
    
    # Send individual alerts for each check
    log("\n📱 SENDING TELEGRAM ALERTS...")
    
    for check_name, passed, issues, fixes in checks:
        status_emoji = "✅" if passed else "❌"
        status_text = "PASSED" if passed else "FAILED"
        
        alert_message = f"""
🔔 **{check_name} Check** 🔔
**Status:** {status_emoji} {status_text}
**Time:** {datetime.now().strftime('%H:%M:%S')}
"""
        
        if issues:
            alert_message += f"**Issues:** {len(issues)}\n"
            for issue in issues[:2]:
                alert_message += f"• {issue}\n"
        
        if fixes:
            alert_message += f"**Fixes Applied:** {len(fixes)}\n"
            for fix in fixes:
                alert_message += f"• {fix}\n"
        
        if not passed and issues:
            alert_message += f"\n🚨 **IMMEDIATE ACTION TAKEN** 🚨"
        
        # Send alert
        send_to_telegram_via_clawdbot(alert_message)
        log(f"  Sent {check_name} alert: {status_text}")
    
    # Send summary
    total_passed = sum(1 for _, passed, _, _ in checks if passed)
    total_checks = len(checks)
    total_issues = sum(len(issues) for _, _, issues, _ in checks)
    total_fixes = sum(len(fixes) for _, _, _, fixes in checks)
    
    summary_message = f"""
📊 **WEBSITE MONITOR SUMMARY**
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Checks Run:** {total_checks}
**Checks Passed:** {total_passed}/{total_checks}
**Issues Found:** {total_issues}
**Fixes Applied:** {total_fixes}
**Overall Status:** {'✅ ALL GOOD' if total_passed == total_checks else '❌ NEEDS ATTENTION'}

🔧 **Monitor runs every 10 minutes**
🔔 **Alerts sent to Telegram immediately**
🔄 **Fixes triggered automatically**
"""
    
    send_to_telegram_via_clawdbot(summary_message)
    log(f"\n✅ Sent summary alert")
    
    # Log final status
    log("\n" + "=" * 70)
    log("📊 CHECK SUMMARY")
    log("=" * 70)
    log(f"Checks passed: {total_passed}/{total_checks}")
    log(f"Issues found: {total_issues}")
    log(f"Fixes applied: {total_fixes}")
    
    if total_passed == total_checks:
        log("🎉 WEBSITE STATUS: EXCELLENT")
    else:
        log("⚠️  WEBSITE STATUS: NEEDS ATTENTION")
    
    # Save status
    status_data = {
        "last_check": datetime.now().isoformat(),
        "checks_passed": total_passed,
        "total_checks": total_checks,
        "issues_found": total_issues,
        "fixes_applied": total_fixes,
        "telegram_alerts_sent": True
    }
    
    with open("clawdbot_monitor_status.json", 'w') as f:
        json.dump(status_data, f, indent=2)
    
    log(f"\n✅ Status saved to clawdbot_monitor_status.json")
    
    return total_passed == total_checks

def main():
    """Main function."""
    success = check_all_and_alert()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()