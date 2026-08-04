#!/bin/bash
# Quick Start Script for Deutsch-Jozsa Quantum Algorithm
# This script sets up the development environment and runs initial tests

set -e  # Exit on error

echo "=========================================="
echo "Deutsch-Jozsa Algorithm - Quick Start"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Production dependencies installed"
echo ""

echo "Installing development dependencies..."
pip install -r requirements-dev.txt --quiet
echo "✓ Development dependencies installed"
echo ""

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install
echo "✓ Pre-commit hooks installed"
echo ""

# Run tests
echo "Running tests..."
pytest tests/ -v --cov=. --cov-report=term-missing
echo ""

# Run the main program
echo "Running Deutsch-Jozsa algorithm..."
python deutsch_jozsa.py
echo ""

echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review the code in deutsch_jozsa.py"
echo "2. Check test results in htmlcov/index.html"
echo "3. Read DEPLOYMENT.md for deployment instructions"
echo "4. See CONTRIBUTING.md for contribution guidelines"
echo ""
echo "To activate the environment later, run:"
echo "  source venv/bin/activate"
echo ""