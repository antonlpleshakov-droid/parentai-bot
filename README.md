# ParentAI Telegram Bot

An AI-powered Telegram bot that provides professional parenting advice for children aged 0-3 years old, based on evidence-based literature and pediatric best practices.

## Features

- 🤖 **AI-Powered Responses**: Uses OpenAI GPT to provide intelligent, contextual advice
- 👶 **Age-Specific Guidance**: Tailored advice based on your child's age (0-3 years)
- 📚 **Evidence-Based**: Knowledge base built from professional parenting literature
- 💬 **Interactive Interface**: Easy-to-use Telegram interface with quick action buttons
- 🚀 **24/7 Availability**: Always available when you need help

## Common Use Cases

1. **Crying Issues**: "Why is my baby crying and what should I do?"
2. **Medical Checkups**: "How often should I take my child to the doctor?"
3. **Age-Appropriate Activities**: "What activities are good for my 6-month-old?"
4. **Sleep Problems**: "How can I help my baby sleep better?"
5. **Feeding Questions**: "When should I introduce solid foods?"

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key

### 2. Installation

```bash
# Clone or download the project
cd parent_ai_bot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Bot

```bash
python main.py
```

## Getting API Keys

### Telegram Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token to your `.env` file

### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## Usage

1. Start a conversation with your bot on Telegram
2. Use `/start` to begin
3. Set your child's age with `/age` for personalized advice
4. Ask any parenting question naturally
5. Use quick action buttons for common topics

## Commands

- `/start` - Start the bot and see welcome message
- `/age` - Set your child's age for personalized advice
- `/topics` - See common topics the bot can help with
- `/help` - Show help information

## Knowledge Base

The bot's knowledge base includes:

- **Crying & Comfort**: Common causes and solutions for different age groups
- **Medical Checkups**: Vaccination schedules and appointment recommendations
- **Age-Appropriate Activities**: Motor skills, cognitive development, and social activities
- **Safety Guidelines**: Childproofing and injury prevention
- **Developmental Milestones**: What to expect at each age

## Deployment

For production deployment, consider using:

- **Railway**: Easy deployment with automatic scaling
- **Heroku**: Popular platform with good Python support
- **DigitalOcean**: VPS with full control
- **AWS/GCP**: Enterprise-grade cloud solutions

## Contributing

This bot is designed to be easily extensible. You can:

1. Add new topics to the knowledge base
2. Improve AI responses with better prompts
3. Add new features like appointment reminders
4. Integrate with external APIs for more data

## Support

If you encounter any issues:

1. Check that all environment variables are set correctly
2. Ensure you have a stable internet connection
3. Verify your API keys are valid and have sufficient credits
4. Check the logs for error messages

## License

This project is open source and available under the MIT License.
