#!/bin/bash
# Start Resume MCP server
# Usage: ./start.sh [static-domain]

PROJECT_DIR=$(cd "$(dirname "$(realpath "$0")")/.." && pwd)
cd "$PROJECT_DIR"

# Kill existing server
pkill -f "server_http.py" 2>/dev/null
sleep 1

# Start server
echo "🚀 Starting server on port 8000..."
python3 "$PROJECT_DIR/server_http.py" > "$PROJECT_DIR/docs/server.log" 2>&1 &
SERVER_PID=$!
echo "  Server PID: $SERVER_PID"
sleep 3

# Check if server started
if ! lsof -i :8000 > /dev/null; then
  echo "  ❌ Server failed. Check docs/server.log"
  exit 1
fi
echo "  ✅ Server started"

# Start ngrok if requested
if [ -n "$1" ]; then
  DOMAIN="$1"
  echo "🌐 Starting ngrok with domain: $DOMAIN"
  pkill -f ngrok 2>/dev/null
  ngrok http --domain="$DOMAIN" 8000 > "$PROJECT_DIR/docs/ngrok.log" 2>&1 &
  sleep 3
  echo "  ✅ ngrok running: https://$DOMAIN/mcp"
elif [ -n "$NGROK_STATIC_DOMAIN" ]; then
  echo "🌐 Starting ngrok with static domain: $NGROK_STATIC_DOMAIN"
  pkill -f ngrok 2>/dev/null
  ngrok http --domain="$NGROK_STATIC_DOMAIN" 8000 > "$PROJECT_DIR/docs/ngrok.log" 2>&1 &
  sleep 3
  echo "  ✅ ngrok running: https://$NGROK_STATIC_DOMAIN/mcp"
else
  echo "💡 To expose with ngrok:"
  echo "   ./start.sh your-domain.ngrok.app"
  echo "   OR set NGROK_STATIC_DOMAIN env var"
fi

echo ""
echo "📋 MCP endpoint: http://localhost:8000/mcp"
echo "🛑 Stop: ./stop.sh"

