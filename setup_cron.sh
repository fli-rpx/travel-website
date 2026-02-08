#!/bin/bash
# Auto-setup cron job for website monitor

SCRIPT_DIR="/Users/fudongli/clawd/travel-website"
MONITOR_SCRIPT="/Users/fudongli/clawd/travel-website/website_monitor.py"
PYTHON_EXEC="/usr/bin/python3"
CRON_ENTRY="*/10 * * * * cd \"$SCRIPT_DIR\" && \"$PYTHON_EXEC\" \"$MONITOR_SCRIPT\" >> \"$SCRIPT_DIR/monitor_cron.log\" 2>&1"

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
