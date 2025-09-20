"""
Main entry point for ParentAI Telegram Bot
"""

import os
import sys
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

def main():
    """Main function to start the bot."""
    print("🤖 Starting ParentAI Telegram Bot...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    try:
        from telegram_bot import ParentAIBot
        bot = ParentAIBot()
        print("✅ Bot initialized successfully!")
        print("🚀 Starting bot polling...")
        bot.run()
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
