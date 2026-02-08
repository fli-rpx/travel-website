#!/bin/bash
# Setup Auto Fix Status Cron Job
# Runs every 10 minutes, sends fix status to Telegram automatically

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEM_SCRIPT="$SCRIPT_DIR/auto_fix_status_system.sh"
CRON_ENTRY="*/10 * * * * cd \"$SCRIPT_DIR\" && \"$SYSTEM_SCRIPT\" >> \"$SCRIPT_DIR/auto_fix_status_cron.log\" 2>&1"

echo "🚀 SETTING UP AUTO FIX STATUS CRON JOB"
echo "=" * 50
echo ""
echo "🎯 **SYSTEM PURPOSE:**"
echo "   • Runs every 10 minutes"
echo "   • Checks website status"
echo "   • Generates fix status report"
echo "   • Sends to Telegram automatically"
echo ""
echo "📱 **TELEGRAM UPDATES INCLUDE:**
echo "   • ✅ What was fixed"
echo "   • ❌ What needs fixing"
echo "   • 🔧 Fixes attempted"
echo "   • 📊 Overall status"
echo "   • ⏰ Next check time"
echo ""
echo "⚡ **AUTOMATIC PROCESS:**
echo "   1. Run website checks"
echo "   2. Generate fix status"
echo "   3. Create Telegram message"
echo "   4. Save for Clawdbot to send"
echo ""
echo "⏰ **SCHEDULE:** Every 10 minutes"
echo "   Next runs: 00:00, 00:10, 00:20, etc."
echo ""
echo "Cron entry:"
echo "$CRON_ENTRY"
echo ""

# Remove existing entry if exists
if crontab -l 2>/dev/null | grep -q "auto_fix_status_system.sh"; then
    echo "🔄 Updating existing cron job..."
    crontab -l 2>/dev/null | grep -v "auto_fix_status_system.sh" | crontab -
fi

# Add new cron entry
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ AUTO FIX STATUS CRON JOB INSTALLED!"
echo ""
echo "📊 Verification:"
echo "   crontab -l | grep auto_fix"
echo ""
echo "📝 Logs:"
echo "   • $SCRIPT_DIR/auto_fix_status.log"
echo "   • $SCRIPT_DIR/auto_fix_status_cron.log"
echo ""
echo "🔧 Test immediately:"
echo "   cd $SCRIPT_DIR"
echo "   ./auto_fix_status_system.sh"
echo ""
echo "👀 Monitor in real-time:"
echo "   tail -f $SCRIPT_DIR/auto_fix_status_cron.log"
echo ""
echo "🎉 **SYSTEM IS NOW ACTIVE!**"
echo "   Next automatic run at: 00:00"
echo "   Telegram fix status will be sent automatically"
echo ""
echo "💡 The system creates:"
echo "   • latest_fix_status.txt - Latest status"
echo "   • send_fix_status_trigger.json - Telegram trigger"
echo "   • Clawdbot will send these to Telegram"