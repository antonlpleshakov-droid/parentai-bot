"""
Simple main entry point for ParentAI Telegram Bot with health check for Railway
"""

import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
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

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for health checks."""
    
    def do_GET(self):
        if self.path in ['/', '/health']:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'ParentAI Bot is running!')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_telegram_bot():
    """Start the Telegram bot in a separate thread."""
    try:
        from telegram_bot import ParentAIBot
        bot = ParentAIBot()
        print("✅ Bot initialized successfully!")
        print("🚀 Starting bot polling...")
        bot.run()
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

def start_health_server():
    """Start the health check HTTP server."""
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"✅ Health check server running on port {port}")
    print("🎉 ParentAI Bot is live and ready!")
    server.serve_forever()

def main():
    """Main function to start both web server and bot."""
    print("🤖 Starting ParentAI Telegram Bot with health check...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Start Telegram bot in a separate thread
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()
    
    # Give the bot a moment to start
    time.sleep(2)
    
    # Start health check server (this will block)
    start_health_server()

if __name__ == "__main__":
    main()
