#!/bin/bash
# Auto Fix Status System
# Runs every 10 minutes, checks website, sends fix status to Telegram

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/auto_fix_status.log"

echo "==========================================" >> "$LOG_FILE"
echo "AUTO FIX STATUS RUN: $(date)" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# Step 1: Run website checks
echo "[$(date '+%H:%M:%S')] Running website checks..." >> "$LOG_FILE"
cd "$SCRIPT_DIR"
python3 enhanced_monitor.py >> "$LOG_FILE" 2>&1

# Step 2: Generate fix status report
echo "[$(date '+%H:%M:%S')] Generating fix status..." >> "$LOG_FILE"
python3 telegram_fix_status_monitor.py >> "$LOG_FILE" 2>&1

# Step 3: Check if fix status was created
if [ -f "$SCRIPT_DIR/telegram_fix_status.json" ]; then
    echo "[$(date '+%H:%M:%S')] Fix status created" >> "$LOG_FILE"
    
    # Extract message from JSON
    MESSAGE=$(python3 -c "
import json
try:
    with open('$SCRIPT_DIR/telegram_fix_status.json', 'r') as f:
        data = json.load(f)
    # Clean the message for Telegram
    msg = data['message']
    # Remove extra newlines and format
    msg = msg.replace('\\\\n\\\\n', '\\\\n').strip()
    print(msg)
except Exception as e:
    print(f'Error: {e}')
")
    
    # Save message to file for Clawdbot to send
    TELEGRAM_MSG_FILE="$SCRIPT_DIR/latest_fix_status.txt"
    echo "$MESSAGE" > "$TELEGRAM_MSG_FILE"
    
    echo "[$(date '+%H:%M:%S')] Fix status saved to $TELEGRAM_MSG_FILE" >> "$LOG_FILE"
    echo "Message size: $(wc -c < "$TELEGRAM_MSG_FILE") bytes" >> "$LOG_FILE"
    
    # Create trigger for Clawdbot
    TRIGGER_FILE="$SCRIPT_DIR/send_fix_status_trigger.json"
    cat > "$TRIGGER_FILE" << EOF
{
  "action": "send",
  "to": "8080442123",
  "channel": "telegram",
  "message": "$(echo "$MESSAGE" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/  */ /g')",
  "timestamp": "$(date -Iseconds)",
  "type": "fix_status_report"
}
EOF
    
    echo "[$(date '+%H:%M:%S')] Trigger file created: $TRIGGER_FILE" >> "$LOG_FILE"
    
else
    echo "[$(date '+%H:%M:%S')] ERROR: Fix status not created" >> "$LOG_FILE"
fi

# Step 4: Save run status
STATUS_FILE="$SCRIPT_DIR/auto_fix_status.json"
cat > "$STATUS_FILE" << EOF
{
  "last_run": "$(date -Iseconds)",
  "log_file": "$LOG_FILE",
  "fix_status_created": "$([ -f "$SCRIPT_DIR/telegram_fix_status.json" ] && echo "true" || echo "false")",
  "next_run": "$(date -d '+10 minutes' -Iseconds)"
}
EOF

echo "[$(date '+%H:%M:%S')] Status saved to $STATUS_FILE" >> "$LOG_FILE"
echo "[$(date '+%H:%M:%S')] Auto fix status system completed" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Print summary to console
echo "✅ Auto Fix Status System completed at $(date '+%H:%M:%S')"
echo "📁 Log: $LOG_FILE"
echo "📱 Fix status ready in: $TELEGRAM_MSG_FILE"
echo "⏰ Next run in 10 minutes"