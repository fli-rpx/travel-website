#!/usr/bin/env python3
"""
Setup cron job to run website monitor every 10 minutes.
"""

import os
import json
from datetime import datetime

def create_cron_job():
    """Create a cron job entry for the website monitor."""
    
    # Get absolute path to the monitor script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    monitor_script = os.path.join(script_dir, "website_monitor.py")
    
    # Python executable path
    python_exec = os.path.realpath("/usr/bin/python3")
    
    # Cron schedule: every 10 minutes
    cron_schedule = "*/10 * * * *"
    
    # Cron command
    cron_command = f'{cron_schedule} cd "{script_dir}" && {python_exec} "{monitor_script}" >> "{script_dir}/monitor_cron.log" 2>&1'
    
    # Create cron setup instructions
    instructions = f"""# WEBSITE MONITOR CRON JOB SETUP
# ==========================================

This cron job will run every 10 minutes to check and improve your travel website.

## CRON ENTRY TO ADD:
{cron_command}

## SETUP INSTRUCTIONS:

### Option 1: Using crontab command
1. Open terminal
2. Run: crontab -e
3. Add the line above
4. Save and exit

### Option 2: Using cron file
1. Create file: /etc/cron.d/travel-website-monitor
2. Add the line above
3. Set permissions: chmod 644 /etc/cron.d/travel-website-monitor

### Option 3: Using launchd (macOS)
1. Create plist file: ~/Library/LaunchAgents/com.travel.website.monitor.plist
2. Use the template below

## macOS LAUNCHD PLIST TEMPLATE:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.travel.website.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_exec}</string>
        <string>{monitor_script}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{script_dir}</string>
    <key>StartInterval</key>
    <integer>600</integer> <!-- 600 seconds = 10 minutes -->
    <key>StandardOutPath</key>
    <string>{script_dir}/monitor_launchd.log</string>
    <key>StandardErrorPath</key>
    <string>{script_dir}/monitor_launchd.error.log</string>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>

## VERIFICATION:
After setup, check logs:
- Cron: tail -f "{script_dir}/monitor_cron.log"
- Launchd: tail -f "{script_dir}/monitor_launchd.log"

## MANUAL TEST:
Run manually to test: {python_exec} "{monitor_script}"
"""
    
    # Save instructions to file
    instructions_file = os.path.join(script_dir, "cron_setup_instructions.txt")
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    # Also create a simple shell script for easy cron setup
    shell_script = f"""#!/bin/bash
# Auto-setup cron job for website monitor

SCRIPT_DIR="{script_dir}"
MONITOR_SCRIPT="{monitor_script}"
PYTHON_EXEC="{python_exec}"
CRON_ENTRY="*/10 * * * * cd \\"$SCRIPT_DIR\\" && \\"$PYTHON_EXEC\\" \\"$MONITOR_SCRIPT\\" >> \\"$SCRIPT_DIR/monitor_cron.log\\" 2>&1"

echo "Setting up website monitor cron job..."
echo "Cron entry: $CRON_ENTRY"
echo ""

# Check if cron entry already exists
if crontab -l 2>/dev/null | grep -q "$MONITOR_SCRIPT"; then
    echo "⚠️  Cron job already exists. Skipping."
else
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo "✅ Cron job added successfully!"
fi

echo ""
echo "To verify: crontab -l"
echo "Logs will be written to: $SCRIPT_DIR/monitor_cron.log"
"""
    
    shell_script_file = os.path.join(script_dir, "setup_cron.sh")
    with open(shell_script_file, 'w', encoding='utf-8') as f:
        f.write(shell_script)
    
    # Make shell script executable
    os.chmod(shell_script_file, 0o755)
    
    return instructions_file, shell_script_file

def create_monitor_config():
    """Create configuration file for the monitor."""
    
    config = {
        "monitor": {
            "enabled": True,
            "check_interval_minutes": 10,
            "max_improvements_per_run": 5,
            "notify_on_issues": True,
            "auto_fix": True
        },
        "checks": {
            "main_page": True,
            "city_pages": True,
            "images": True,
            "links": True,
            "performance": False  # Can be enabled later
        },
        "improvements": {
            "fix_broken_images": True,
            "create_missing_pages": True,
            "update_styles": True,
            "optimize_images": False  # Can be enabled later
        },
        "logging": {
            "level": "INFO",
            "max_log_files": 10,
            "max_log_size_mb": 10
        }
    }
    
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monitor_config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    return config_file

def main():
    """Setup complete monitoring system."""
    
    print("=" * 60)
    print("WEBSITE MONITOR CRON JOB SETUP")
    print("=" * 60)
    
    print("\n🎯 Setting up automated website monitoring...")
    
    # Create monitor config
    config_file = create_monitor_config()
    print(f"✅ Created config: {config_file}")
    
    # Create cron setup files
    instructions_file, shell_script_file = create_cron_job()
    print(f"✅ Created instructions: {instructions_file}")
    print(f"✅ Created setup script: {shell_script_file}")
    
    # Test the monitor
    print("\n🔧 Testing monitor script...")
    try:
        import subprocess
        result = subprocess.run(
            ["python3", "website_monitor.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Monitor test passed!")
        else:
            print(f"⚠️ Monitor test completed with code: {result.returncode}")
        
        # Show last few lines of output
        lines = result.stdout.strip().split('\n')
        if lines:
            print("\nLast output lines:")
            for line in lines[-5:]:
                print(f"  {line}")
    
    except Exception as e:
        print(f"❌ Monitor test failed: {e}")
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE - NEXT STEPS")
    print("=" * 60)
    
    print("\n📋 To enable automated monitoring every 10 minutes:")
    print(f"1. Run: chmod +x {shell_script_file}")
    print(f"2. Run: {shell_script_file}")
    print("   OR")
    print("3. Follow instructions in: cron_setup_instructions.txt")
    
    print("\n🔍 Manual testing:")
    print("   cd travel-website && python3 website_monitor.py")
    
    print("\n📊 Monitor will:")
    print("   • Check website every 10 minutes")
    print("   • Find and fix issues automatically")
    print("   • Log all activities")
    print("   • Maintain website quality")
    
    print("\n✅ Your website now has automated quality control!")
    print("   It will continuously improve itself.")

if __name__ == "__main__":
    main()