#!/usr/bin/env python3
"""
Fix Telegram Automation
- Runs after each 10-minute check
- Sends fix status to Telegram automatically
- Uses Clawdbot's message API
"""

import os
import json
import sys
from datetime import datetime

def send_fix_status_to_telegram():
    """Send the latest fix status to Telegram."""
    
    print("=" * 60)
    print("🔧 FIXING TELEGRAM AUTOMATION")
    print("=" * 60)
    
    # Check if latest fix status exists
    status_file = "latest_fix_status.txt"
    if not os.path.exists(status_file):
        print("❌ No fix status file found")
        return False
    
    # Read the fix status
    with open(status_file, 'r', encoding='utf-8') as f:
        fix_status = f.read().strip()
    
    print(f"✅ Found fix status ({len(fix_status)} chars)")
    print(f"📅 Generated at: {os.path.getmtime(status_file)}")
    
    # Check if this is a new status (less than 5 minutes old)
    file_age = datetime.now().timestamp() - os.path.getmtime(status_file)
    if file_age > 300:  # 5 minutes
        print(f"⚠️  Status is {file_age:.0f} seconds old (may be stale)")
    
    # Try to send via Clawdbot
    try:
        # Import Clawdbot message tool
        sys.path.append('/opt/homebrew/lib/node_modules/clawdbot')
        from clawdbot.tools.message import send_message
        
        print("📱 Attempting to send to Telegram...")
        
        result = send_message(
            action='send',
            to='8080442123',
            channel='telegram',
            message=fix_status
        )
        
        if result.get('ok'):
            print(f"✅ Telegram sent successfully! (ID: {result.get('messageId')})")
            
            # Mark as sent
            with open("telegram_sent_status.json", "w") as f:
                json.dump({
                    "last_sent": datetime.now().isoformat(),
                    "message_id": result.get('messageId'),
                    "status_file": status_file,
                    "file_age_seconds": file_age
                }, f, indent=2)
            
            return True
        else:
            print(f"❌ Telegram failed: {result}")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not send Telegram: {e}")
        
        # Save for manual sending
        pending_file = "pending_telegram_fixes.txt"
        with open(pending_file, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Time: {datetime.now().isoformat()}\n")
            f.write(f"Status file: {status_file}\n")
            f.write(f"File age: {file_age:.0f} seconds\n")
            f.write(f"{fix_status}\n")
        
        print(f"💾 Saved to {pending_file} for manual sending")
        return False

def check_system_status():
    """Check overall system status."""
    print("\n🔍 CHECKING SYSTEM STATUS")
    print("-" * 40)
    
    files_to_check = [
        "auto_fix_status_cron.log",
        "latest_fix_status.txt", 
        "enhanced_monitor_cron.log",
        "auto_fix_status.json"
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            mtime = datetime.fromtimestamp(os.path.getmtime(file))
            age = (datetime.now() - mtime).total_seconds()
            
            status = "✅" if age < 600 else "⚠️ "  # Less than 10 minutes
            print(f"{status} {file}: {size:,} bytes, {age:.0f}s ago")
        else:
            print(f"❌ {file}: Missing")
    
    # Check cron job
    print("\n⏰ CRON JOB STATUS")
    print("-" * 40)
    
    try:
        import subprocess
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )
        
        if "auto_fix_status_system.sh" in result.stdout:
            print("✅ Cron job is installed")
            # Find the schedule
            for line in result.stdout.split('\n'):
                if "auto_fix_status_system.sh" in line:
                    print(f"   Schedule: {line.strip()}")
        else:
            print("❌ Cron job not found in crontab")
            
    except Exception as e:
        print(f"⚠️  Could not check cron: {e}")

def main():
    """Main function."""
    print(f"\n🚀 TELEGRAM AUTOMATION FIX")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check system status
    check_system_status()
    
    # Send latest fix status
    print("\n📱 SENDING LATEST FIX STATUS")
    print("-" * 40)
    
    success = send_fix_status_to_telegram()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TELEGRAM AUTOMATION FIXED!")
        print("• Fix status sent successfully")
        print("• System will send automatically next time")
    else:
        print("⚠️  MANUAL INTERVENTION NEEDED")
        print("• Fix status saved to pending_telegram_fixes.txt")
        print("• Check system configuration")
    
    print(f"\n⏰ Next scheduled check: 00:20")
    print("=" * 60)

if __name__ == "__main__":
    main()