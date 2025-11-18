#!/bin/bash
# Security scan before pushing to GitHub

echo "🔍 Security Scan Before GitHub Push"
echo ""

# Check for .env file
if [ -f .env ]; then
    echo "⚠️  .env file exists (should be in .gitignore)"
    if git check-ignore .env > /dev/null; then
        echo "✅ .env is properly ignored"
    else
        echo "❌ .env is NOT ignored! Add to .gitignore"
        exit 1
    fi
else
    echo "✅ No .env file found"
fi

# Check for API keys in committed files
echo ""
echo "🔍 Scanning for API keys in committed files..."
KEYS_FOUND=$(git ls-files | xargs grep -l "f91aab4749d6f8dcc7b91d8d983278fa8b9b4ba6944cf4c0a21632f6395b7115\|128438458c46cec459439b2adddca362db36b6e48bfe4e608d3ba1e25c5f32f4\|GQqvqi4jkzlPlJjRnwXOIeMk" 2>/dev/null | wc -l)

if [ "$KEYS_FOUND" -gt 0 ]; then
    echo "❌ Found API keys in committed files!"
    git ls-files | xargs grep -l "f91aab4749d6f8dcc7b91d8d983278fa8b9b4ba6944cf4c0a21632f6395b7115\|128438458c46cec459439b2adddca362db36b6e48bfe4e608d3ba1e25c5f32f4\|GQqvqi4jkzlPlJjRnwXOIeMk" 2>/dev/null
    exit 1
else
    echo "✅ No API keys found in committed files"
fi

# Run semgrep
echo ""
echo "🔍 Running semgrep security scan..."
if command -v semgrep &> /dev/null; then
    semgrep --config=auto --error . 2>&1 | head -30
    echo ""
    echo "✅ Semgrep scan complete"
else
    echo "⚠️  semgrep not installed (optional)"
fi

echo ""
echo "✅ Security check complete - safe to push!"
