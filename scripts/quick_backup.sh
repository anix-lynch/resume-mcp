#!/bin/bash
# Quick backup script for Resume MCP

echo "💾 Quick Backup Script"
echo ""

# Check if git repo
if [ -d .git ]; then
    echo "✅ Git repo found"
    
    # Check if remote exists
    if git remote -v | grep -q origin; then
        echo "✅ GitHub remote configured"
        echo ""
        echo "📤 Pushing to GitHub..."
        git add .
        git commit -m "Backup: $(date +%Y-%m-%d\ %H:%M:%S)" || echo "No changes to commit"
        git push
        echo "✅ Pushed to GitHub!"
    else
        echo "⚠️  No GitHub remote configured"
        echo ""
        echo "🔗 To add GitHub remote:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/resume-mcp.git"
        echo "   git push -u origin main"
    fi
else
    echo "⚠️  Not a git repo"
    echo ""
    echo "🔧 To initialize:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
fi

echo ""
echo "💡 Your checklist is safe in:"
echo "   - Local files (CHECKLIST.md)"
if [ -d .git ]; then
    echo "   - Git history (version control)"
    if git remote -v | grep -q origin; then
        echo "   - GitHub (cloud backup)"
    fi
fi
echo "   - Vercel (deployed code)"
