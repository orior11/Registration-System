#!/bin/bash

# Quick Start Script for Authentication API

echo "🚀 Starting Authentication API..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your actual credentials before running again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check JWT_SECRET
if grep -q "your-secret-key-here-change-this-in-production" .env; then
    echo ""
    echo "⚠️  WARNING: You're using the default JWT_SECRET!"
    echo "   Generate a secure one with:"
    echo "   python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    echo ""
fi

# Start the server
echo ""
echo "✅ Starting server..."
echo "📍 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
