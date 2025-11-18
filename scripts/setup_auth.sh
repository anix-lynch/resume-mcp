#!/bin/bash
# Setup authentication for Resume MCP

echo "🔐 Setting up authentication..."
echo ""

# Generate secure API keys
OWNER_KEY=$(openssl rand -hex 32)
PUBLIC_KEY=$(openssl rand -hex 32)

echo "✅ Generated API Keys:"
echo ""
echo "OWNER_API_KEY=$OWNER_KEY"
echo "PUBLIC_API_KEY=$PUBLIC_KEY"
echo ""

# Save to .env file
cat > .env << EOF
# Authentication Keys
# Owner key: Full access (automatic for you via Vercel SSO)
OWNER_API_KEY=$OWNER_KEY

# Public key: Limited access (for others)
PUBLIC_API_KEY=$PUBLIC_KEY

# Vercel bypass secret (if using deployment protection)
VERCEL_BYPASS_SECRET=
EOF

echo "📝 Saved to .env file"
echo ""
echo "💡 Next steps:"
echo "1. Add these to Vercel environment variables:"
echo "   - OWNER_API_KEY"
echo "   - PUBLIC_API_KEY"
echo ""
echo "2. For Vercel SSO (automatic auth for you):"
echo "   - Keep deployment protection ON"
echo "   - You'll be auto-authenticated via Vercel SSO"
echo ""
echo "3. For others:"
echo "   - Share PUBLIC_API_KEY"
echo "   - Use in requests: X-API-Key header or ?api_key=..."
echo ""

