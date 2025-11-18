#!/bin/bash
# Quick Vercel deployment script

echo "🚀 Deploying to Vercel..."
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm i -g vercel
fi

echo "📋 Deploying..."
vercel

echo ""
echo "✅ Deployment complete!"
echo ""
echo "💡 To deploy to production:"
echo "   vercel --prod"
echo ""
echo "💡 To add custom domain:"
echo "   vercel domains add resume.gozeroshot.dev"
