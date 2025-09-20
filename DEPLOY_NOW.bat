@echo off
echo.
echo ========================================
echo    PARENTAI BOT - QUICK DEPLOYMENT
echo ========================================
echo.

echo Step 1: Getting API Keys...
echo.
echo 1. TELEGRAM BOT TOKEN:
echo    - Go to https://t.me/botfather
echo    - Send /newbot
echo    - Follow instructions
echo    - Copy the token
echo.
echo 2. OPENAI API KEY:
echo    - Go to https://platform.openai.com
echo    - Sign up/login
echo    - Go to API Keys
echo    - Create new key
echo    - Copy the key
echo.

pause

echo.
echo Step 2: Deploying to Railway...
echo.
echo 1. Go to https://railway.app
echo 2. Sign up with GitHub
echo 3. Click "New Project" -> "Deploy from GitHub repo"
echo 4. Create new repository and upload these files
echo 5. Add environment variables:
echo    - TELEGRAM_BOT_TOKEN = your bot token
echo    - OPENAI_API_KEY = your OpenAI key
echo 6. Click Deploy
echo.

pause

echo.
echo Step 3: Testing your bot...
echo.
echo 1. Find your bot on Telegram
echo 2. Send /start
echo 3. Test with sample questions
echo.

echo ========================================
echo    YOUR BOT WILL BE LIVE IN 2 MINUTES!
echo ========================================
echo.

pause
