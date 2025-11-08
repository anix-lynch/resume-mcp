#!/bin/bash
# Start recruiter-friendly web interface

PROJECT_DIR=$(dirname "$(realpath "$0")")
cd "$PROJECT_DIR"

echo "🚀 Starting Recruiter Interface on port 8001..."

# Check if port 8001 is in use
if lsof -i :8001 > /dev/null; then
  echo "⚠️  Port 8001 already in use. Killing existing process..."
  pkill -f "recruiter_interface.py"
  sleep 2
fi

# Start recruiter interface
python3 recruiter_interface.py > recruiter_interface.log 2>&1 &
INTERFACE_PID=$!
echo "  Interface PID: $INTERFACE_PID"

sleep 3

# Check if it started
if lsof -i :8001 > /dev/null; then
  echo "✅ Recruiter interface started!"
  echo ""
  echo "📋 Local URL: http://localhost:8001"
  echo ""
  echo "🌐 To expose publicly, run ngrok on port 8001:"
  echo "   ngrok http 8001"
  echo ""
  echo "💡 Then share the ngrok URL with recruiters!"
else
  echo "❌ Failed to start. Check recruiter_interface.log"
  cat recruiter_interface.log
fi
