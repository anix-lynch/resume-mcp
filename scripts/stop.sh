#!/bin/bash
# Stop Resume MCP server and ngrok

pkill -f "server_http.py"
pkill -f "ngrok http"
echo "✅ Stopped"

