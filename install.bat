@echo off
REM Installation script for PDF Processor (Windows)

echo.
echo ================================
echo   PDF Processor Setup (Windows)
echo ================================
echo.

REM Check Python version
echo Checking Python version...
python --version 2>&1
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
python -m pip install --upgrade pip setuptools wheel > nul 2>&1
echo.

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo Dependencies installed
echo.

REM Create directories
echo Creating directories...
if not exist "uploads" mkdir uploads
if not exist "output" mkdir output
if not exist "logs" mkdir logs
echo.

REM Copy environment file
echo Setting up environment...
if not exist ".env" (
    copy .env.example .env
    echo Environment file created (.env)
) else (
    echo Environment file already exists
)
echo.

echo ================================
echo   Setup Complete! ✓
echo ================================
echo.
echo To start the application, run:
echo.
echo   venv\Scripts\activate.bat
echo   python run_web.py
echo.
echo Then open: http://localhost:5000
echo.
pause
