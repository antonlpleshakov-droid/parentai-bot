"""
Main entry point for ParentAI Telegram Bot with health check for Railway
"""

import os
import sys
import asyncio
import threading
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
    return web.Response(text="Enhanced ParentAI Bot is running!", status=200)

def start_telegram_bot():
    """Start the Telegram bot in a separate thread."""
    try:
        from enhanced_telegram_bot import EnhancedParentAIBot
        bot = EnhancedParentAIBot()
        print("✅ Enhanced bot initialized successfully!")
        print("🚀 Starting enhanced bot polling...")
        bot.run()
    except Exception as e:
        print(f"❌ Error starting enhanced bot: {e}")
        print("Falling back to basic bot...")
        try:
            from telegram_bot import ParentAIBot
            bot = ParentAIBot()
            print("✅ Basic bot initialized successfully!")
            print("🚀 Starting basic bot polling...")
            bot.run()
        except Exception as e2:
            print(f"❌ Error starting basic bot: {e2}")

async def init_app():
    """Initialize the web application with health check."""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    return app

def main():
    """Main function to start both web server and bot."""
    print("🤖 Starting Enhanced ParentAI Telegram Bot with health check...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Start Telegram bot in a separate thread
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()
    
    # Start web server for health checks
    async def start_web_server():
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
    
    # Run the web server
    asyncio.run(start_web_server())

if __name__ == "__main__":
    main()