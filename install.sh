#!/bin/bash
# Installation script for PDF Processor

set -e

echo ""
echo "================================"
echo "  PDF Processor Setup"
echo "================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $python_version"

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo "  Virtual environment activated"

# Upgrade pip
echo ""
echo "✓ Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt
echo "  Dependencies installed"

# Create directories
echo ""
echo "✓ Creating directories..."
mkdir -p uploads output logs

# Copy environment file
echo ""
echo "✓ Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  Environment file created (.env)"
else
    echo "  Environment file already exists"
fi

echo ""
echo "================================"
echo "  Setup Complete! ✓"
echo "================================"
echo ""
echo "To start the application, run:"
echo ""
echo "  source venv/bin/activate"
echo "  python run_web.py"
echo ""
echo "Then open: http://localhost:5000"
echo ""
