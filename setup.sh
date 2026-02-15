#!/bin/bash

# AI Flow Video Generator - Complete Setup Script
# This script sets up everything needed for deployment

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   🎬 AI Flow Video Generator - Setup Script          ║"
echo "║   Gemini Flow-like video transitions                  ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check Python installation
echo "🔍 Checking requirements..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi
print_success "Python found: $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip is not installed!"
    echo "Please install pip"
    exit 1
fi
print_success "pip found"

echo ""
echo "📋 What would you like to do?"
echo "1. 🚀 Quick Start - Run locally (Lite version)"
echo "2. 📦 Full Setup - Install everything"
echo "3. 🧪 Run Tests"
echo "4. 🌐 Deploy to Koyeb - Generate deployment files"
echo "5. ❓ Help"
echo ""
read -p "Select option [1-5]: " option

case $option in
    1)
        echo ""
        echo "🚀 Quick Start - Installing dependencies..."
        pip3 install -r requirements-lite.txt --quiet
        print_success "Dependencies installed"
        
        echo ""
        echo "✨ Starting AI Flow (Lite version)..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🌐 Open your browser and visit:"
        echo "   http://localhost:8000"
        echo ""
        echo "Press Ctrl+C to stop the server"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        python3 app_lite.py
        ;;
        
    2)
        echo ""
        echo "📦 Full Setup..."
        
        # Create virtual environment
        read -p "Create virtual environment? (recommended) [Y/n]: " create_venv
        if [[ ! $create_venv =~ ^[Nn]$ ]]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
            source venv/bin/activate || . venv/Scripts/activate 2>/dev/null
            print_success "Virtual environment created and activated"
        fi
        
        # Install dependencies
        echo ""
        echo "Installing Python dependencies..."
        pip3 install -r requirements-lite.txt
        print_success "Dependencies installed"
        
        # Run tests
        echo ""
        echo "Running tests..."
        python3 test.py
        
        echo ""
        print_success "Setup complete!"
        echo ""
        echo "To start the app:"
        echo "  python3 app_lite.py"
        echo ""
        echo "To deploy to Koyeb:"
        echo "  ./setup.sh (option 4)"
        ;;
        
    3)
        echo ""
        echo "🧪 Running tests..."
        python3 test.py
        ;;
        
    4)
        echo ""
        echo "🌐 Preparing for Koyeb deployment..."
        
        # Check if git is initialized
        if [ ! -d .git ]; then
            print_info "Git repository not initialized"
            read -p "Initialize git repository? [Y/n]: " init_git
            if [[ ! $init_git =~ ^[Nn]$ ]]; then
                git init
                print_success "Git repository initialized"
            fi
        fi
        
        # Create .gitignore if not exists
        if [ ! -f .gitignore ]; then
            cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
venv/
.env
*.log
.DS_Store
test_*.mp4
EOF
            print_success "Created .gitignore"
        fi
        
        echo ""
        print_info "For Koyeb deployment, use these files:"
        echo "  ✓ app_lite.py (main application)"
        echo "  ✓ requirements-lite.txt (dependencies)"
        echo "  ✓ Dockerfile.lite (Docker configuration)"
        echo "  ✓ templates/ (frontend)"
        echo ""
        
        echo "📚 Deployment Steps:"
        echo ""
        echo "1. Push to GitHub:"
        echo "   git add ."
        echo "   git commit -m 'AI Flow Video Generator'"
        echo "   git remote add origin YOUR_REPO_URL"
        echo "   git push -u origin main"
        echo ""
        echo "2. On Koyeb Dashboard:"
        echo "   - Create new app"
        echo "   - Connect GitHub repo"
        echo "   - Builder: Docker"
        echo "   - Dockerfile: Dockerfile.lite"
        echo "   - Port: 8000"
        echo "   - Instance: Nano (Free tier)"
        echo ""
        echo "3. Deploy!"
        echo ""
        
        read -p "Open deployment guide in browser? [Y/n]: " open_guide
        if [[ ! $open_guide =~ ^[Nn]$ ]]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open "DEPLOYMENT.md" &>/dev/null &
            elif command -v open &> /dev/null; then
                open "DEPLOYMENT.md" &>/dev/null &
            fi
        fi
        
        print_info "See DEPLOYMENT.md for complete guide"
        ;;
        
    5)
        echo ""
        echo "❓ Help & Documentation"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "📚 Available Documentation:"
        echo "  • README.md - Main documentation"
        echo "  • QUICK_START.md - Quick reference guide"
        echo "  • DEPLOYMENT.md - Koyeb deployment guide"
        echo "  • PROJECT_OVERVIEW.md - Complete overview"
        echo ""
        echo "🚀 Quick Commands:"
        echo "  • Start app: python3 app_lite.py"
        echo "  • Run tests: python3 test.py"
        echo "  • Setup: ./setup.sh"
        echo ""
        echo "🌐 URLs:"
        echo "  • Local: http://localhost:8000"
        echo "  • Koyeb: https://koyeb.com"
        echo "  • GitHub: Push your repo"
        echo ""
        echo "💡 Tips:"
        echo "  • Use lite version for free hosting"
        echo "  • 8-16 frames for best performance"
        echo "  • Check DEPLOYMENT.md for step-by-step guide"
        echo ""
        ;;
        
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_success "Done!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
