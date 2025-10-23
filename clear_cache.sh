#!/bin/bash
# TTZ.KT AI - Cache Clear Script
# Use this when you get "attribute 'UPPER'" error

echo "🧹 Clearing Python cache..."

# Remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Remove all .pyc files
find . -type f -name "*.pyc" -delete 2>/dev/null

# Remove .streamlit cache
rm -rf .streamlit/cache 2>/dev/null

echo "✅ Cache cleared!"
echo ""
echo "Now restart your app:"
echo "  streamlit run app.py"
