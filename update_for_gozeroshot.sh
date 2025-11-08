#!/bin/bash
# Update scripts to use resume.gozeroshot.dev

PROJECT_DIR=$(dirname "$(realpath "$0")")
cd "$PROJECT_DIR"

DOMAIN="resume.gozeroshot.dev"

echo "🔧 Updating for domain: $DOMAIN"
echo ""

# Save to .ngrok_domain file
echo "NGROK_STATIC_DOMAIN=$DOMAIN" > .ngrok_domain
echo "✅ Saved domain to .ngrok_domain"

echo ""
echo "📋 Your URLs will be:"
echo "   MCP API: https://$DOMAIN/mcp"
echo "   Web UI: https://$DOMAIN/"
echo "   ChatGPT: https://$DOMAIN/mcp"
echo ""

echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Add domain in ngrok dashboard: $DOMAIN"
echo "   2. Add CNAME record in your domain provider (Vercel/Google/etc)"
echo "   3. Wait for DNS propagation (5-60 min)"
echo "   4. Verify in ngrok dashboard"
echo "   5. Start server: ./start_resume_mcp_static.sh"
