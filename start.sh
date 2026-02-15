#!/bin/bash

echo "🎬 AI Flow Video Generator - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed!"
    echo "Please install pip"
    exit 1
fi

echo "✅ pip found"
echo ""

# Create virtual environment (optional but recommended)
read -p "Create virtual environment? (recommended) [y/N]: " create_venv

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    echo "✅ Virtual environment activated"
    echo ""
fi

# Install dependencies
read -p "Install dependencies? [Y/n]: " install_deps

if [[ ! $install_deps =~ ^[Nn]$ ]]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements-lite.txt
    echo "✅ Dependencies installed"
    echo ""
fi

# Run tests
read -p "Run tests? [Y/n]: " run_tests

if [[ ! $run_tests =~ ^[Nn]$ ]]; then
    echo "🧪 Running tests..."
    python3 test.py
    echo ""
fi

# Ask to start the app
echo "Ready to start the app!"
echo ""
echo "Options:"
echo "1. Run locally (Lite version - CPU)"
echo "2. Run locally (Full version - requires GPU)"
echo "3. Exit and deploy to Koyeb"
echo ""

read -p "Select option [1-3]: " option

case $option in
    1)
        echo "🚀 Starting Lite version..."
        echo "Visit http://localhost:8000 in your browser"
        echo "Press Ctrl+C to stop"
        echo ""
        python3 app_lite.py
        ;;
    2)
        echo "🚀 Starting Full version..."
        echo "Note: This requires GPU and large models!"
        echo "Visit http://localhost:8000 in your browser"
        echo "Press Ctrl+C to stop"
        echo ""
        python3 app.py
        ;;
    3)
        echo ""
        echo "📚 To deploy to Koyeb:"
        echo "1. Read DEPLOYMENT.md for full guide"
        echo "2. Push to GitHub: git push origin main"
        echo "3. Deploy on Koyeb dashboard"
        echo ""
        echo "Quick commands:"
        echo "  git init"
        echo "  git add ."
        echo "  git commit -m 'Initial commit'"
        echo "  git branch -M main"
        echo "  git remote add origin YOUR_REPO_URL"
        echo "  git push -u origin main"
        echo ""
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac
