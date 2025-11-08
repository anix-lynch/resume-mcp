#!/bin/bash
# Quick script to check if you can find your domain

echo "🔍 Checking ngrok status..."
echo ""

# Check if ngrok is running
if curl -s http://localhost:4040/api/tunnels > /dev/null 2>&1; then
  echo "✅ ngrok is running locally"
  echo ""
  echo "Current tunnel URLs:"
  curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tunnels = data.get('tunnels', [])
    if tunnels:
        for tunnel in tunnels:
            url = tunnel.get('public_url', '')
            config = tunnel.get('config', {})
            addr = config.get('addr', '')
            print(f'  URL: {url}')
            print(f'  Points to: {addr}')
            print('')
    else:
        print('  No active tunnels')
except Exception as e:
    print(f'  Error: {e}')
" 2>/dev/null
else
  echo "ℹ️  ngrok not running locally"
  echo ""
fi

echo "📋 To get your STATIC DOMAIN:"
echo "   1. Go to: https://dashboard.ngrok.com"
echo "   2. Click 'Domains' in sidebar"
echo "   3. Copy your domain (e.g., anix-resume.ngrok-free.app)"
echo "   4. Tell me the domain name!"
echo ""
echo "💡 The static domain is different from the random tunnel URL above"
echo "   Static domain = never changes, set once in dashboard"
echo "   Random URL = changes every restart (free tier)"
