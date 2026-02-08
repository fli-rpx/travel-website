#!/usr/bin/env python3
"""
Send latest fix status to Telegram via Clawdbot.
Run this from within Clawdbot.
"""

import sys
import os

# Read the status
status_file = "/Users/fudongli/clawd/travel-website/latest_fix_status.txt"
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
