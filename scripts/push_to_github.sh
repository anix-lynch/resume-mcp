#!/bin/bash
# Push Resume MCP to GitHub

GITHUB_USER="godmode1"
REPO_NAME="resume-mcp"

echo "🚀 Pushing to GitHub..."
echo ""
echo "📋 Repo: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""

# Check if remote exists
if git remote -v | grep -q origin; then
    echo "✅ Remote already configured"
    git remote -v
else
    echo "🔗 Adding GitHub remote..."
    git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git
fi

echo ""
echo "📤 Pushing to GitHub..."
echo "⚠️  Note: If repo doesn't exist, create it first at:"
echo "   https://github.com/new"
echo "   Name: $REPO_NAME"
echo "   Make it Private (recommended for resume data)"
echo ""

# Try to push
if git push -u origin main 2>&1; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 View at: https://github.com/$GITHUB_USER/$REPO_NAME"
else
    echo ""
    echo "⚠️  Push failed. Common reasons:"
    echo "   1. Repo doesn't exist yet - create it at https://github.com/new"
    echo "   2. Authentication needed - use GitHub CLI or SSH keys"
    echo ""
    echo "💡 To create repo via GitHub CLI:"
    echo "   gh repo create $REPO_NAME --private --source=. --remote=origin --push"
fi
