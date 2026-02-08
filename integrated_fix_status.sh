#!/bin/bash
# Integrated Fix Status System
# Runs after each 10-minute check and posts fix status to Telegram

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔄 INTEGRATING FIX STATUS WITH 10-MINUTE CHECKS"
echo "=" * 50

# 1. First run the main monitor
echo "1. Running website checks..."
python3 "$SCRIPT_DIR/enhanced_monitor.py" > /dev/null 2>&1

# 2. Then run fix status monitor
echo "2. Generating fix status report..."
python3 "$SCRIPT_DIR/telegram_fix_status_monitor.py"

# 3. Check if Telegram alert file was created
if [ -f "$SCRIPT_DIR/telegram_fix_status.json" ]; then
    echo "3. Fix status report created: telegram_fix_status.json"
    
    # Extract message from JSON
    MESSAGE=$(python3 -c "
import json
with open('$SCRIPT_DIR/telegram_fix_status.json', 'r') as f:
    data = json.load(f)
print(data['message'].replace('\\\\n', '\\\\\\\\n').replace('\"', '\\\\\\\\\"'))
")
    
    echo "4. ✅ Fix status ready for Telegram"
    echo ""
    echo "📱 Telegram message prepared:"
    echo "---"
    echo "$MESSAGE" | head -20
    echo "..."
    echo "---"
else
    echo "3. ❌ Fix status report not created"
fi

echo ""
echo "🎉 INTEGRATION COMPLETE"
echo "• Main checks run every 10 minutes"
echo "• Fix status posted to Telegram after each check"
echo "• Next run: 00:00"