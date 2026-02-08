#!/bin/bash
# Simple Telegram Sender
# Sends the latest fix status to Telegram
# Can be called from cron or manually

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATUS_FILE="$SCRIPT_DIR/latest_fix_status.txt"
LOG_FILE="$SCRIPT_DIR/telegram_sender.log"

echo "==========================================" >> "$LOG_FILE"
echo "TELEGRAM SENDER RUN: $(date)" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# Check if status file exists
if [ ! -f "$STATUS_FILE" ]; then
    echo "[$(date '+%H:%M:%S')] ERROR: No status file found" >> "$LOG_FILE"
    echo "❌ No status file found"
    exit 1
fi

# Read status
STATUS_CONTENT=$(cat "$STATUS_FILE")
STATUS_SIZE=${#STATUS_CONTENT}

echo "[$(date '+%H:%M:%S')] Status file: $STATUS_FILE ($STATUS_SIZE chars)" >> "$LOG_FILE"

# Create a simple Python script that Clawdbot can run
PYTHON_SCRIPT="$SCRIPT_DIR/send_telegram_now.py"
cat > "$PYTHON_SCRIPT" << EOF
#!/usr/bin/env python3
"""
Send latest fix status to Telegram via Clawdbot.
Run this from within Clawdbot.
"""

import sys
import os

# Read the status
status_file = "$STATUS_FILE"
with open(status_file, 'r', encoding='utf-8') as f:
    message = f.read().strip()

print(f"📱 Sending fix status ({len(message)} chars)...")

# This will be executed by Clawdbot
# The actual sending happens when Clawdbot runs this script
print("MESSAGE_TO_SEND:")
print(message)
print("END_MESSAGE")

# Also save to a trigger file
trigger_file = os.path.join(os.path.dirname(status_file), "telegram_trigger.txt")
with open(trigger_file, 'w') as f:
    f.write(message)

print(f"✅ Trigger saved to {trigger_file}")
EOF

chmod +x "$PYTHON_SCRIPT"

echo "[$(date '+%H:%M:%S')] Created Python script: $PYTHON_SCRIPT" >> "$LOG_FILE"

# Create a simple command file for Clawdbot
CMD_FILE="$SCRIPT_DIR/clawdbot_send_command.txt"
cat > "$CMD_FILE" << EOF
# Command for Clawdbot to send fix status
# Run this command in Clawdbot:

cd /Users/fudongli/clawd/travel-website
python3 send_telegram_now.py

# Or manually send this message:
$STATUS_CONTENT
EOF

echo "[$(date '+%H:%M:%S')] Created command file: $CMD_FILE" >> "$LOG_FILE"

# Also create a direct message file
MSG_FILE="$SCRIPT_DIR/direct_message.txt"
echo "$STATUS_CONTENT" > "$MSG_FILE"

echo "[$(date '+%H:%M:%S')] Created direct message: $MSG_FILE" >> "$LOG_FILE"

# Print summary
echo "✅ Telegram sender prepared files:"
echo "   • $PYTHON_SCRIPT - Python script for Clawdbot"
echo "   • $CMD_FILE - Command instructions"
echo "   • $MSG_FILE - Direct message content"
echo "   • $LOG_FILE - Execution log"
echo ""
echo "📱 To send manually from Clawdbot:"
echo "   cd /Users/fudongli/clawd/travel-website"
echo "   python3 send_telegram_now.py"
echo ""
echo "⏰ Next scheduled check: 00:20"
echo "🔄 System will prepare files automatically"

echo "[$(date '+%H:%M:%S')] Telegram sender completed" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"