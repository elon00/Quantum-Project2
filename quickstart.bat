@echo off
REM Quick Start Script for Deutsch-Jozsa Quantum Algorithm (Windows)
REM This script sets up the development environment and runs initial tests

echo ==========================================
echo Deutsch-Jozsa Algorithm - Quick Start
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Production dependencies installed
echo.

echo Installing development dependencies...
pip install -r requirements-dev.txt --quiet
echo Development dependencies installed
echo.

REM Install pre-commit hooks
echo Installing pre-commit hooks...
pre-commit install
echo Pre-commit hooks installed
echo.

REM Run tests
echo Running tests...
pytest tests/ -v --cov=. --cov-report=term-missing
echo.

REM Run the main program
echo Running Deutsch-Jozsa algorithm...
python deutsch_jozsa.py
echo.

echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Review the code in deutsch_jozsa.py
echo 2. Check test results in htmlcov\index.html
echo 3. Read DEPLOYMENT.md for deployment instructions
echo 4. See CONTRIBUTING.md for contribution guidelines
echo.
echo To activate the environment later, run:
echo   venv\Scripts\activate.bat
echo.
pause