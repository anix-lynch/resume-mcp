#!/bin/bash
# Quick setup script - run this after you get your ngrok static domain

echo "🚀 ngrok Static Domain Setup"
echo "============================"
echo ""

# Check if domain is already set
if [ -n "$NGROK_STATIC_DOMAIN" ]; then
  echo "✅ Domain already set: $NGROK_STATIC_DOMAIN"
  echo ""
  read -p "Use this domain? (y/n): " use_existing
  if [ "$use_existing" != "y" ]; then
    unset NGROK_STATIC_DOMAIN
  fi
fi

# Get domain from user
if [ -z "$NGROK_STATIC_DOMAIN" ]; then
  echo "Enter your ngrok static domain:"
  echo "  (e.g., anix-resume.ngrok-free.app)"
  read -p "Domain: " domain_input
  
  if [ -z "$domain_input" ]; then
    echo "❌ Domain required. Exiting."
    exit 1
  fi
  
  export NGROK_STATIC_DOMAIN="$domain_input"
fi

# Save to shell config
SHELL_CONFIG="$HOME/.zshrc"
if [ -f "$HOME/.bashrc" ]; then
  SHELL_CONFIG="$HOME/.bashrc"
fi

# Check if already in config
if ! grep -q "NGROK_STATIC_DOMAIN" "$SHELL_CONFIG" 2>/dev/null; then
  echo ""
  echo "💾 Saving to $SHELL_CONFIG for permanent use..."
  echo "export NGROK_STATIC_DOMAIN=$NGROK_STATIC_DOMAIN" >> "$SHELL_CONFIG"
  echo "✅ Saved! (will be available in new terminals)"
fi

# Save to .env file for scripts
echo "NGROK_STATIC_DOMAIN=$NGROK_STATIC_DOMAIN" > .ngrok_domain
echo "✅ Saved to .ngrok_domain"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Your static domain: $NGROK_STATIC_DOMAIN"
echo "📋 Your MCP URL: https://$NGROK_STATIC_DOMAIN/mcp"
echo ""
echo "🚀 Starting server with static domain..."
echo ""

# Start the server
./start_resume_mcp_static.sh
