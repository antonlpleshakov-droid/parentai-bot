@echo off
echo Starting ParentAI Telegram Bot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo .env file not found!
    echo Please create .env file with your API keys
    echo See README.md for instructions
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing dependencies...
pip install -r requirements.txt

REM Run the bot
echo Starting bot...
python main.py

pause
