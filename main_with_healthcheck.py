"""
Main entry point for ParentAI Telegram Bot with health check for Railway
"""

import os
import sys
import asyncio
from aiohttp import web
from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY

def check_environment():
    """Check if required environment variables are set."""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in environment variables")
        print("Please set your Telegram bot token in the .env file")
        return False
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in the .env file")
        return False
    
    return True

async def health_check(request):
    """Health check endpoint for Railway."""
    return web.Response(text="ParentAI Bot is running! 🤖", status=200)

async def start_bot():
    """Start the Telegram bot."""
    try:
        from telegram_bot import ParentAIBot
        bot = ParentAIBot()
        print("✅ Bot initialized successfully!")
        print("🚀 Starting bot polling...")
        
        # Start the bot in the background
        asyncio.create_task(bot.application.run_polling())
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        return False
    
    return True

async def init_app():
    """Initialize the web application with health check."""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    return app

async def main():
    """Main function to start both web server and bot."""
    print("🤖 Starting ParentAI Telegram Bot with health check...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Start the bot
    bot_started = await start_bot()
    if not bot_started:
        sys.exit(1)
    
    # Start web server for health checks
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Get port from Railway or use default
    port = int(os.environ.get('PORT', 8000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f"✅ Health check server running on port {port}")
    print("🎉 ParentAI Bot is live and ready!")
    
    # Keep the application running
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        print("🛑 Shutting down...")
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
