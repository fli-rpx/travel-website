#!/bin/bash
# Setup enhanced cron job for website monitoring
# Checks every 10 minutes: images, pages, layout consistency

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITOR_SCRIPT="$SCRIPT_DIR/enhanced_monitor.py"
PYTHON_EXEC="/usr/bin/python3"
CRON_ENTRY="*/10 * * * * cd \"$SCRIPT_DIR\" && \"$PYTHON_EXEC\" \"$MONITOR_SCRIPT\" >> \"$SCRIPT_DIR/enhanced_monitor_cron.log\" 2>&1"

echo "🔧 Setting up ENHANCED website monitor cron job..."
echo "This will check every 10 minutes:"
echo "  1. Images readiness for each city"
echo "  2. Pages readiness for each city"
echo "  3. Layout and color consistency between pages"
echo ""
echo "Cron entry:"
echo "$CRON_ENTRY"
echo ""

# Check if cron entry already exists
if crontab -l 2>/dev/null | grep -q "enhanced_monitor.py"; then
    echo "⚠️  Enhanced cron job already exists. Updating..."
    # Remove existing entry
    crontab -l 2>/dev/null | grep -v "enhanced_monitor.py" | crontab -
fi

# Add new cron entry
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Enhanced cron job added successfully!"
echo ""
echo "📊 To verify: crontab -l"
echo "📝 Logs will be written to: $SCRIPT_DIR/enhanced_monitor_cron.log"
echo ""
echo "🔍 To test immediately:"
echo "   cd $SCRIPT_DIR"
echo "   python3 enhanced_monitor.py"
echo ""
echo "👀 To view logs:"
echo "   tail -f $SCRIPT_DIR/enhanced_monitor_cron.log"