#!/bin/bash
# Start script with static ngrok domain (for paid plans)
# Usage: ./start_resume_mcp_static.sh

PROJECT_DIR=$(dirname "$(realpath "$0")")

# Function to check if a port is in use
is_port_in_use() {
  lsof -i :$1 > /dev/null
}

# Function to kill process on a port
kill_process_on_port() {
  PID=$(lsof -t -i :$1)
  if [ -n "$PID" ]; then
    echo "Killing process $PID on port $1..."
    kill -9 $PID
    sleep 1
  fi
}

echo "=========================================="
echo "🚀 Starting Resume MCP (Static Domain)"
echo "=========================================="

cd "$PROJECT_DIR"

# Check if static domain is configured
if [ -z "$NGROK_STATIC_DOMAIN" ]; then
  # Try to load from .ngrok_domain file
  if [ -f ".ngrok_domain" ]; then
    source .ngrok_domain
  fi
fi

if [ -z "$NGROK_STATIC_DOMAIN" ]; then
  echo ""
  echo "⚠️  NGROK_STATIC_DOMAIN not set!"
  echo ""
  echo "To use static domain:"
  echo "  1. Get ngrok paid plan: https://ngrok.com/pricing"
  echo "  2. Get your static domain from ngrok dashboard"
  echo "  3. Run: ./quick_setup_after_purchase.sh"
  echo "     OR set manually:"
  echo "     export NGROK_STATIC_DOMAIN=yourname.ngrok-free.app"
  echo "  4. Run this script again"
  echo ""
  echo "Or use regular start: ./start_resume_mcp.sh"
  exit 1
fi

# Stop any existing server on port 8000
kill_process_on_port 8000

# Start the combined HTTP server in the background
echo "🚀 Starting server on port 8000..."
python3 server_http.py > server.log 2>&1 &
SERVER_PID=$!
echo "  Server PID: $SERVER_PID"

# Wait for the server to start
sleep 5

# Check if server started successfully
if ! is_port_in_use 8000; then
  echo "  ❌ Server failed to start. Check server.log:"
  cat server.log
  exit 1
fi
echo "  ✅ Server started"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null
then
    echo "ngrok could not be found. Please install it: https://ngrok.com/download"
    exit 1
fi

# Check if ngrok is already running with this domain
NGROK_RUNNING=$(pgrep -f "ngrok.*$NGROK_STATIC_DOMAIN" || true)

if [ -z "$NGROK_RUNNING" ]; then
  # Kill any other ngrok instances
  pkill -f ngrok 2>/dev/null
  sleep 1
  
  # Start ngrok with static domain
  echo "🌐 Starting ngrok with static domain: $NGROK_STATIC_DOMAIN"
  ngrok http --domain="$NGROK_STATIC_DOMAIN" 8000 > ngrok.log 2>&1 &
  NGROK_PID=$!
  echo "  ngrok PID: $NGROK_PID"
  
  # Wait for ngrok to start
  sleep 5
else
  echo "🌐 ngrok already running with static domain"
  echo "  ✅ URL is: https://$NGROK_STATIC_DOMAIN"
fi

STATIC_URL="https://$NGROK_STATIC_DOMAIN"

echo ""
echo "✅ SUCCESS! Server running with static domain"
echo ""
echo "📋 MCP Server URL for ChatGPT (NEVER CHANGES!):"
echo "   ${STATIC_URL}/mcp"
echo ""
echo "💾 URL saved to ngrok_url.txt"
echo "${STATIC_URL}/mcp" > ngrok_url.txt

echo ""
echo "🔧 Available Tools (14 total):"
echo "   Resume MCP: get_resume_info, match_jobs, get_shortlist, get_skills, check_job_match"
echo "   B Past Life: get_b_past_life_resume_info, check_b_past_life_job_match"
echo "   Northstar: get_northstar_info, list_projects, get_project, get_project_by_name,"
echo "              get_shared_assets, get_ai_agent_plan, search_projects"
echo ""
echo "💡 This URL will NEVER change! Set it once in ChatGPT and forget it."
echo ""
echo "📁 Log files:"
echo "   - server.log"
echo "   - ngrok.log"
echo ""
echo "🛑 To stop:"
echo "   ./stop_resume_mcp.sh"

