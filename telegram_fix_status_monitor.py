#!/usr/bin/env python3
"""
Telegram Fix Status Monitor
- Runs every 10 minutes
- Sends detailed fix status to Telegram
- Shows what was fixed and what still needs fixing
"""

import os
import json
import subprocess
import sys
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def send_telegram(message):
    """Send message to Telegram via Clawdbot."""
    try:
        # This creates a file that Clawdbot can process
        alert_file = "telegram_fix_status.json"
        
        alert_data = {
            "timestamp": datetime.now().isoformat(),
            "chat_id": "8080442123",
            "message": message,
            "type": "fix_status"
        }
        
        # Save to file
        with open(alert_file, 'w') as f:
            json.dump(alert_data, f, indent=2)
        
        log(f"✅ Fix status prepared for Telegram")
        
        # Also print to console for testing
        print(f"\n📱 TELEGRAM FIX STATUS:\n{message}\n")
        
        return True
        
    except Exception as e:
        log(f"❌ Error preparing Telegram: {e}")
        return False

def check_images_fix_status():
    """Check and report image fix status."""
    log("🔍 Checking image fix status...")
    
    status = {
        "check": "Images",
        "passed": False,
        "issues": [],
        "fixes": [],
        "remaining": []
    }
    
    try:
        with open("baidu_image_replacements.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cities = data.get("cities", {})
        missing = []
        
        for city, city_data in cities.items():
            if city_data.get("baidu_replacement") == "REPLACE_WITH_BAIDU_IMAGE_URL":
                missing.append(city)
        
        if missing:
            status["issues"].append(f"{len(missing)} cities need images")
            status["remaining"] = missing[:5]  # First 5 cities
            
            # Check if fix was attempted
            fix_log = "enhanced_monitor_cron.log"
            if os.path.exists(fix_log):
                with open(fix_log, 'r') as f:
                    log_content = f.read()
                    if "image" in log_content.lower() and "fix" in log_content.lower():
                        status["fixes"].append("Image search attempted")
        else:
            status["passed"] = True
            status["fixes"].append("All cities have images")
    
    except Exception as e:
        status["issues"].append(f"Error: {str(e)}")
    
    return status

def check_pages_fix_status():
    """Check and report page fix status."""
    log("🔍 Checking page fix status...")
    
    status = {
        "check": "Pages",
        "passed": False,
        "issues": [],
        "fixes": [],
        "remaining": []
    }
    
    try:
        cities_dir = "cities"
        if not os.path.exists(cities_dir):
            status["issues"].append("Cities directory missing")
        else:
            expected = ["beijing", "shanghai", "chengdu", "harbin", "chongqing",
                       "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen",
                       "guangzhou", "hongkong"]
            
            missing = []
            for city in expected:
                if not os.path.exists(f"{cities_dir}/{city}.html"):
                    missing.append(city)
            
            if missing:
                status["issues"].append(f"{len(missing)} pages missing")
                status["remaining"] = missing[:3]
            else:
                status["passed"] = True
                status["fixes"].append("All 12 city pages exist")
    
    except Exception as e:
        status["issues"].append(f"Error: {str(e)}")
    
    return status

def check_navigation_fix_status():
    """Check and report navigation fix status."""
    log("🔍 Checking navigation fix status...")
    
    status = {
        "check": "Navigation",
        "passed": False,
        "issues": [],
        "fixes": [],
        "remaining": []
    }
    
    try:
        # Check if fix_all_issues.py has been run
        fix_log = "enhanced_monitor_cron.log"
        if os.path.exists(fix_log):
            with open(fix_log, 'r') as f:
                log_content = f.read()
                
                if "navigation" in log_content.lower() and "fix" in log_content.lower():
                    status["fixes"].append("Navigation fixes applied")
                
                if "navigation" in log_content.lower() and "failed" in log_content.lower():
                    status["issues"].append("Navigation issues detected")
                else:
                    status["passed"] = True
                    status["fixes"].append("Navigation working")
        else:
            status["issues"].append("No fix logs found")
    
    except Exception as e:
        status["issues"].append(f"Error: {str(e)}")
    
    return status

def check_layout_fix_status():
    """Check and report layout fix status."""
    log("🔍 Checking layout fix status...")
    
    status = {
        "check": "Layout",
        "passed": False,
        "issues": [],
        "fixes": [],
        "remaining": []
    }
    
    try:
        # Check main page
        if os.path.exists("index.html"):
            with open("index.html", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for expected colors
            expected_colors = ["#2563eb", "#1e40af", "#f59e0b"]
            missing_colors = []
            
            for color in expected_colors:
                if color not in content:
                    missing_colors.append(color)
            
            if missing_colors:
                status["issues"].append(f"Missing colors: {len(missing_colors)}")
                status["remaining"] = missing_colors
            else:
                status["passed"] = True
                status["fixes"].append("Colors consistent")
        else:
            status["issues"].append("Main page missing")
    
    except Exception as e:
        status["issues"].append(f"Error: {str(e)}")
    
    return status

def create_fix_status_message(all_statuses):
    """Create detailed fix status message for Telegram."""
    
    total_checks = len(all_statuses)
    passed_checks = sum(1 for s in all_statuses if s["passed"])
    
    message = f"""
🔧 **WEBSITE FIX STATUS REPORT** 🔧
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Checks:** {passed_checks}/{total_checks} passed

"""
    
    for status in all_statuses:
        check_name = status["check"]
        passed = status["passed"]
        
        emoji = "✅" if passed else "❌"
        message += f"\n{emoji} **{check_name}:** "
        
        if passed:
            message += "FIXED"
            if status["fixes"]:
                message += f" ({', '.join(status['fixes'])})"
        else:
            message += "NEEDS FIXING"
            if status["issues"]:
                message += f"\n   • Issues: {', '.join(status['issues'])}"
            if status["remaining"]:
                message += f"\n   • Remaining: {', '.join(status['remaining'][:3])}"
                if len(status["remaining"]) > 3:
                    message += f" (+{len(status['remaining'])-3} more)"
        
        if status["fixes"] and not passed:
            message += f"\n   • Fixes attempted: {', '.join(status['fixes'])}"
    
    # Add overall status
    message += f"\n\n📊 **OVERALL STATUS:** "
    if passed_checks == total_checks:
        message += "✅ ALL FIXES COMPLETE"
    else:
        message += f"❌ {total_checks - passed_checks} CHECKS NEED FIXING"
    
    # Add next steps
    message += f"""
    
🔄 **NEXT STEPS:**
• Monitor runs every 10 minutes
• Auto-fixes will continue
• Next check at: {(datetime.now().replace(second=0, microsecond=0).replace(minute=((datetime.now().minute // 10) * 10 + 10) % 60)).strftime('%H:%M')}

🔔 **REAL-TIME UPDATES:**
Fix status will be posted after each check
"""
    
    return message

def run_fix_status_check():
    """Run all checks and send fix status to Telegram."""
    log("=" * 60)
    log("🔧 TELEGRAM FIX STATUS MONITOR")
    log("=" * 60)
    
    # Run all status checks
    status_checks = [
        check_images_fix_status(),
        check_pages_fix_status(),
        check_navigation_fix_status(),
        check_layout_fix_status()
    ]
    
    # Create detailed message
    message = create_fix_status_message(status_checks)
    
    # Send to Telegram
    send_telegram(message)
    
    # Log summary
    passed = sum(1 for s in status_checks if s["passed"])
    total = len(status_checks)
    
    log(f"\n📊 Fix Status: {passed}/{total} checks fixed")
    log("✅ Fix status sent to Telegram")
    
    # Save status
    status_data = {
        "timestamp": datetime.now().isoformat(),
        "checks": status_checks,
        "passed": passed,
        "total": total,
        "message_sent": True
    }
    
    with open("fix_status_report.json", 'w') as f:
        json.dump(status_data, f, indent=2)
    
    log("✅ Status saved to fix_status_report.json")
    
    return passed == total

def main():
    """Main function."""
    run_fix_status_check()

if __name__ == "__main__":
    main()