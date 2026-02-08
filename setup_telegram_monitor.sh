#!/bin/bash
# Setup Telegram-enabled website monitor
# Runs every 10 minutes, sends alerts to Telegram, triggers immediate fixes

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITOR_SCRIPT="$SCRIPT_DIR/telegram_monitor.py"
PYTHON_EXEC="/usr/bin/python3"
CRON_ENTRY="*/10 * * * * cd \"$SCRIPT_DIR\" && \"$PYTHON_EXEC\" \"$MONITOR_SCRIPT\" >> \"$SCRIPT_DIR/telegram_monitor_cron.log\" 2>&1"

echo "🔔 Setting up TELEGRAM-ENABLED website monitor..."
echo ""
echo "🎯 Features:"
echo "   • Runs every 10 minutes"
echo "   • Sends immediate alerts to Telegram"
echo "   • Triggers fixes automatically"
echo "   • 4 specific checks:"
echo "     1. Images readiness for each city"
echo "     2. Pages readiness for each city"
echo "     3. Layout & color consistency"
echo "     4. Navigation link correctness"
echo ""
echo "📱 Telegram alerts sent to: 8080442123"
echo ""
echo "Cron entry:"
echo "$CRON_ENTRY"
echo ""

# Remove existing telegram monitor cron entry if exists
if crontab -l 2>/dev/null | grep -q "telegram_monitor.py"; then
    echo "⚠️  Telegram monitor already exists. Updating..."
    crontab -l 2>/dev/null | grep -v "telegram_monitor.py" | crontab -
fi

# Add new cron entry
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Telegram-enabled monitor cron job added!"
echo ""
echo "📊 To verify: crontab -l"
echo "📝 Logs will be written to: $SCRIPT_DIR/telegram_monitor_cron.log"
echo ""
echo "🔍 To test immediately (sends Telegram alert):"
echo "   cd $SCRIPT_DIR"
echo "   python3 telegram_monitor.py"
echo ""
echo "👀 To view logs:"
echo "   tail -f $SCRIPT_DIR/telegram_monitor_cron.log"
echo ""
echo "🔄 Next scheduled run:"
echo "   Every 10 minutes (e.g., 23:50, 00:00, 00:10, etc.)"
echo ""
echo "🎉 Telegram alerts will start immediately!"