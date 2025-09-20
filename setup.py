"""
Setup script for ParentAI Telegram Bot
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_env_file():
    """Create .env file template."""
    env_file = ".env"
    if os.path.exists(env_file):
        print("⚠️  .env file already exists. Skipping creation.")
        return True
    
    env_content = """# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Bot Configuration
BOT_NAME=ParentAI
BOT_DESCRIPTION=Your AI assistant for parenting questions about children 0-3 years old
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 Please edit .env file and add your API keys")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up ParentAI Telegram Bot...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your API keys")
    print("2. Get a Telegram bot token from @BotFather")
    print("3. Get an OpenAI API key from platform.openai.com")
    print("4. Run: python main.py")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main()
