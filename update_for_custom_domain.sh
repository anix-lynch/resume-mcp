#!/bin/bash
# Update scripts to use custom domain anixlynch.com

PROJECT_DIR=$(dirname "$(realpath "$0")")
cd "$PROJECT_DIR"

echo "🔧 Updating for custom domain: anixlynch.com"
echo ""

# Ask which subdomain to use
echo "Which subdomain do you want to use?"
echo "  1. resume.anixlynch.com (for recruiter interface)"
echo "  2. mcp.anixlynch.com (for MCP server)"
echo "  3. custom (enter your own)"
read -p "Choice (1-3): " choice

case $choice in
  1)
    DOMAIN="resume.anixlynch.com"
    ;;
  2)
    DOMAIN="mcp.anixlynch.com"
    ;;
  3)
    read -p "Enter subdomain (e.g., resume): " subdomain
    DOMAIN="${subdomain}.anixlynch.com"
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac

echo ""
echo "✅ Using domain: $DOMAIN"
echo ""

# Save to .ngrok_domain file
echo "NGROK_STATIC_DOMAIN=$DOMAIN" > .ngrok_domain
echo "✅ Saved domain to .ngrok_domain"

# Update start script to use custom domain
echo ""
echo "📋 Your MCP URL will be:"
echo "   https://$DOMAIN/mcp"
echo ""
echo "📋 Your Recruiter Interface URL will be:"
echo "   https://$DOMAIN"
echo ""

echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Make sure DNS is configured in Google Domains"
echo "   2. Verify domain in ngrok dashboard (should show 'Active')"
echo "   3. Start server: ./start_resume_mcp_static.sh"
echo "   4. Update ChatGPT with: https://$DOMAIN/mcp"
