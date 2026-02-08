#!/bin/bash
# Test GitHub Pages deployment locally

echo "🔍 Testing GitHub Pages deployment locally..."
echo ""

# Start local server in background
python3 -m http.server 8000 > /dev/null 2>&1 &
SERVER_PID=$!

echo "✅ Local server started (PID: $SERVER_PID)"
echo ""

# Wait for server to start
sleep 2

echo "🌐 Testing URLs:"
echo ""

# Test main page
echo "1. Main page:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/
echo " http://localhost:8000/"

# Test a few city pages
CITIES=("guangzhou" "beijing" "shanghai" "chengdu" "harbin")

for city in "${CITIES[@]}"; do
    echo -n "$city: "
    curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/cities/${city}.html
    echo " http://localhost:8000/cities/${city}.html"
done

echo ""
echo "📱 Open in browser:"
echo "   Main: http://localhost:8000/"
echo "   Guangzhou: http://localhost:8000/cities/guangzhou.html"
echo ""

# Kill server
kill $SERVER_PID 2>/dev/null
echo "✅ Server stopped"

echo ""
echo "🚀 To deploy to GitHub Pages:"
echo "   cd /Users/fudongli/clawd/travel-website"
echo "   git add ."
echo "   git commit -m 'Fix GitHub Pages deployment'"
echo "   git push origin main"
echo ""
echo "🌐 After push (wait 1-2 minutes):"
echo "   Test: https://fli-rpx.github.io/travel-website/cities/guangzhou.html"