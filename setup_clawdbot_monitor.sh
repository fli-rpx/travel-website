#!/bin/bash
# Setup Clawdbot-Integrated Website Monitor
# Runs every 10 minutes, sends Telegram alerts immediately, triggers fixes

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITOR_SCRIPT="$SCRIPT_DIR/clawdbot_integrated_monitor.py"
PYTHON_EXEC="/usr/bin/python3"
CRON_ENTRY="*/10 * * * * cd \"$SCRIPT_DIR\" && \"$PYTHON_EXEC\" \"$MONITOR_SCRIPT\" >> \"$SCRIPT_DIR/clawdbot_monitor_cron.log\" 2>&1"

echo "🚀 SETTING UP CLAWDBOT-INTEGRATED MONITOR"
echo "=" * 50
echo ""
echo "🎯 **YOUR REQUEST IMPLEMENTED:**"
echo "   • Checks every 10 minutes"
echo "   • Results sent to Telegram IMMEDIATELY"
echo "   • Fixes triggered automatically after checks"
echo ""
echo "🔍 **4 CHECKS PERFORMED:**"
echo "   1. Images readiness for each city"
echo "   2. Pages readiness for each city"
echo "   3. Navigation link correctness"
echo "   4. Layout & color consistency"
echo ""
echo "📱 **TELEGRAM ALERTS SENT TO:** 8080442123"
echo ""
echo "⚡ **IMMEDIATE ACTION:**"
echo "   • Issues trigger Telegram alerts instantly"
echo "   • Auto-fixes attempted immediately"
echo "   • You get notified in real-time"
echo ""
echo "⏰ **SCHEDULE:** Every 10 minutes (23:50, 00:00, 00:10, etc.)"
echo ""
echo "Cron entry:"
echo "$CRON_ENTRY"
echo ""

# Remove existing entry if exists
if crontab -l 2>/dev/null | grep -q "clawdbot_integrated_monitor.py"; then
    echo "🔄 Updating existing monitor..."
    crontab -l 2>/dev/null | grep -v "clawdbot_integrated_monitor.py" | crontab -
fi

# Add new cron entry
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ CLAWDBOT-INTEGRATED MONITOR INSTALLED!"
echo ""
echo "📊 Verification:"
echo "   crontab -l | grep clawdbot"
echo ""
echo "📝 Logs: $SCRIPT_DIR/clawdbot_monitor_cron.log"
echo ""
echo "🔧 Test immediately (sends Telegram alerts):"
echo "   cd $SCRIPT_DIR"
echo "   python3 clawdbot_integrated_monitor.py"
echo ""
echo "👀 Monitor logs in real-time:"
echo "   tail -f $SCRIPT_DIR/clawdbot_monitor_cron.log"
echo ""
echo "🎉 **SYSTEM IS NOW ACTIVE!**"
echo "   Next check at: 23:50"
echo "   Telegram alerts will arrive immediately"
echo "   Fixes will be attempted automatically"