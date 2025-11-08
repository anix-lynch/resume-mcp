#!/bin/bash

# Stop the combined Resume MCP server

echo "🛑 Stopping Combined Resume MCP server..."

# Kill server
pkill -f "server_http.py"
sleep 2

# Kill ngrok
pkill -f ngrok
sleep 2

echo "✅ Server and ngrok stopped"
echo ""
echo "To restart, run: ./start_resume_mcp.sh"

