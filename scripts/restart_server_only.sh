#!/bin/bash
# Restart only the Python server, keep ngrok running
# This preserves your ngrok URL!

PROJECT_DIR=$(cd "$(dirname "$(realpath "$0")")/.." && pwd)
cd "$PROJECT_DIR"

echo "🔄 Restarting server only (keeping ngrok running)..."

# Kill only the Python server
pkill -f server_http.py
sleep 2

# Start server again
python3 "$PROJECT_DIR/server_http.py" > "$PROJECT_DIR/docs/server.log" 2>&1 &
SERVER_PID=$!
echo "  ✅ Server restarted (PID: $SERVER_PID)"

# Wait for server to start
sleep 3

# Get current ngrok URL (should be the same!)
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null)

if [ -n "$NGROK_URL" ] && [ "$NGROK_URL" != "null" ]; then
  echo ""
  echo "✅ Server restarted!"
  echo "📋 Your ngrok URL (unchanged):"
  echo "   ${NGROK_URL}/mcp"
  echo ""
  echo "💡 No need to update ChatGPT - URL is the same!"
else
  echo "⚠️  ngrok might not be running. Start with: ./start_resume_mcp.sh"
fi

