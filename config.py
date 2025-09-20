import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Bot Configuration
BOT_NAME = "ParentAI"
BOT_DESCRIPTION = "Ваш помощник по воспитанию детей, основанный на книге Людмилы Петрановской 'Тайная опора'"

# Knowledge base configuration
KNOWLEDGE_BASE_PATH = "knowledge_base/"
