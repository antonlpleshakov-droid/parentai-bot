"""
Deployment helper script for ParentAI Bot
"""

import os
import subprocess
import sys

def check_git():
    """Check if git is installed and initialized."""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install Git first.")
        return False

def init_git_repo():
    """Initialize git repository if not already initialized."""
    if os.path.exists(".git"):
        print("✅ Git repository already initialized")
        return True
    
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit - ParentAI Bot"], check=True)
        print("✅ Git repository initialized and initial commit created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error initializing git: {e}")
        return False

def create_env_template():
    """Create .env template file."""
    env_content = """# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Bot Configuration
BOT_NAME=ParentAI
BOT_DESCRIPTION=Your AI assistant for parenting questions about children 0-3 years old
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    print("✅ .env template created")

def show_deployment_instructions():
    """Show deployment instructions."""
    print("\n" + "="*60)
    print("🚀 PARENTAI BOT DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    
    print("\n1️⃣ GET YOUR API KEYS:")
    print("   • Telegram Bot Token: Message @BotFather on Telegram")
    print("   • OpenAI API Key: Get from platform.openai.com")
    
    print("\n2️⃣ DEPLOY TO RAILWAY (RECOMMENDED):")
    print("   • Go to railway.app and sign up with GitHub")
    print("   • Push this code to GitHub:")
    print("     git remote add origin YOUR_GITHUB_REPO_URL")
    print("     git push -u origin main")
    print("   • Connect Railway to your GitHub repo")
    print("   • Add environment variables in Railway dashboard:")
    print("     - TELEGRAM_BOT_TOKEN")
    print("     - OPENAI_API_KEY")
    print("   • Deploy!")
    
    print("\n3️⃣ ALTERNATIVE - DEPLOY TO HEROKU:")
    print("   • Install Heroku CLI")
    print("   • Run: heroku create your-parentai-bot")
    print("   • Run: heroku config:set TELEGRAM_BOT_TOKEN=your_token")
    print("   • Run: heroku config:set OPENAI_API_KEY=your_key")
    print("   • Run: git push heroku main")
    
    print("\n4️⃣ TEST YOUR BOT:")
    print("   • Find your bot on Telegram")
    print("   • Send /start command")
    print("   • Test with sample questions")
    
    print("\n" + "="*60)
    print("🎉 Your bot will be live 24/7 once deployed!")
    print("="*60)

def main():
    """Main deployment function."""
    print("🚀 Preparing ParentAI Bot for deployment...")
    
    # Check git
    if not check_git():
        return False
    
    # Initialize git repo
    if not init_git_repo():
        return False
    
    # Create env template
    create_env_template()
    
    # Show instructions
    show_deployment_instructions()
    
    return True

if __name__ == "__main__":
    main()
