"""Quick start guide for running GARUDA."""

#!/bin/bash

set -e

echo "🚀 GARUDA Quick Start"
echo "====================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "✓ Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt

# Run setup script
echo "✓ Running setup..."
python setup.py

echo ""
echo "✅ Quick start completed!"
echo ""
echo "To start the API server, run:"
echo "  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "To train models, run:"
echo "  python training/train_models.py"
echo ""
