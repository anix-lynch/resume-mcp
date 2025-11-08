#!/bin/bash

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
echo "🚀 Starting Combined Resume MCP Server"
echo "=========================================="

cd "$PROJECT_DIR"

# Stop any existing server on port 8000 (but keep ngrok running!)
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

# Check if ngrok is already running
NGROK_RUNNING=$(pgrep -f "ngrok http 8000" || true)

if [ -z "$NGROK_RUNNING" ]; then
  # Start ngrok in the background (only if not already running)
  echo "🌐 Starting ngrok..."
  ngrok http 8000 > ngrok.log 2>&1 &
  NGROK_PID=$!
  echo "  ngrok PID: $NGROK_PID"
  
  # Wait for ngrok to start and get the public URL
  echo "⏳ Waiting for ngrok API..."
  sleep 5 # Give ngrok time to establish tunnel
else
  echo "🌐 ngrok already running (PID: $NGROK_RUNNING)"
  echo "  ✅ Keeping existing tunnel - URL stays the same!"
fi

NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null)

if [ -z "$NGROK_URL" ] || [ "$NGROK_URL" == "null" ]; then
  echo "❌ Failed to get ngrok public URL. Check ngrok.log:"
  cat ngrok.log
  exit 1
fi

echo "✅ SUCCESS! Your combined server is exposed via ngrok"
echo ""
echo "📋 MCP Server URL for ChatGPT:"
echo "   ${NGROK_URL}/mcp"
echo ""

# Save URL to file for easy reference
echo "${NGROK_URL}/mcp" > ngrok_url.txt
echo "💾 URL saved to ngrok_url.txt"

echo ""
echo "🔧 Available Tools (14 total):"
echo "   Resume MCP: get_resume_info, match_jobs, get_shortlist, get_skills, check_job_match"
echo "   B Past Life: get_b_past_life_resume_info, check_b_past_life_job_match"
echo "   Northstar: get_northstar_info, list_projects, get_project, get_project_by_name,"
echo "              get_shared_assets, get_ai_agent_plan, search_projects"
echo ""
echo "💡 TIP: Keep ngrok running! Only restart the Python server when needed."
echo "   This keeps your URL the same in ChatGPT."
echo ""
echo "📁 Log files:"
echo "   - server.log"
echo "   - ngrok.log"
echo ""
echo "🛑 To stop:"
echo "   ./stop_resume_mcp.sh"
