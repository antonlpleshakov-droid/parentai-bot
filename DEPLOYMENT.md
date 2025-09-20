# ParentAI Bot Deployment Guide

This guide will help you deploy your ParentAI Telegram bot to various cloud platforms for 24/7 availability.

## Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Push your code to GitHub
   - Connect Railway to your GitHub repo
   - Railway will auto-detect Python and install dependencies

3. **Set Environment Variables**
   - In Railway dashboard, go to your project
   - Add these environment variables:
     - `TELEGRAM_BOT_TOKEN`: Your bot token from @BotFather
     - `OPENAI_API_KEY`: Your OpenAI API key

4. **Deploy**
   - Railway will automatically deploy and give you a URL
   - Your bot will be running 24/7!

### Option 2: Heroku

1. **Install Heroku CLI**
   - Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create Heroku App**
   ```bash
   heroku create your-parentai-bot
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_token_here
   heroku config:set OPENAI_API_KEY=your_key_here
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

### Option 3: DigitalOcean App Platform

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://digitalocean.com)

2. **Create New App**
   - Connect your GitHub repository
   - Select Python as the runtime
   - Set environment variables

3. **Deploy**
   - DigitalOcean will build and deploy automatically

## Local Development Setup

If you want to run the bot locally for testing:

### 1. Install Python
- Download Python 3.8+ from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment
Create a `.env` file:
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
2. Send `/newbot`
3. Follow the instructions to create your bot
4. Copy the bot token

### OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key

## Testing Your Bot

1. **Test Locally First**
   ```bash
   python test_bot.py
   ```

2. **Test with Real Bot**
   - Start your bot
   - Message your bot on Telegram
   - Try commands like `/start`, `/age`, `/help`

## Monitoring and Maintenance

### Railway
- Check logs in Railway dashboard
- Monitor usage and costs
- Set up alerts for errors

### Heroku
- Use `heroku logs --tail` to see logs
- Monitor dyno usage
- Set up log monitoring

### General Tips
- Monitor API usage and costs
- Set up error notifications
- Regular backups of user data
- Update dependencies regularly

## Troubleshooting

### Common Issues

1. **Bot Not Responding**
   - Check if environment variables are set correctly
   - Verify API keys are valid
   - Check logs for errors

2. **Import Errors**
   - Make sure all dependencies are installed
   - Check Python version compatibility

3. **API Rate Limits**
   - Monitor OpenAI API usage
   - Implement rate limiting if needed

4. **Memory Issues**
   - Monitor memory usage
   - Optimize code if needed

### Getting Help

- Check the logs for error messages
- Verify all environment variables are set
- Test API keys independently
- Check platform-specific documentation

## Production Considerations

1. **Security**
   - Never commit API keys to version control
   - Use environment variables for all secrets
   - Implement proper error handling

2. **Performance**
   - Monitor response times
   - Implement caching if needed
   - Optimize AI prompts

3. **Scalability**
   - Monitor user growth
   - Plan for increased API costs
   - Consider database for user data

4. **Reliability**
   - Set up health checks
   - Implement proper error handling
   - Plan for downtime scenarios

## Cost Estimation

### Railway
- Free tier: $5/month credit
- Pro: $20/month + usage

### Heroku
- Free tier: Limited hours
- Basic: $7/month per dyno

### OpenAI API
- GPT-3.5-turbo: ~$0.002 per 1K tokens
- Typical cost: $5-20/month for moderate usage

### Total Estimated Cost
- **Low usage**: $10-15/month
- **Moderate usage**: $25-40/month
- **High usage**: $50-100/month

## Next Steps

1. Deploy your bot using one of the methods above
2. Test thoroughly with real users
3. Monitor performance and costs
4. Iterate and improve based on feedback
5. Consider adding more features like:
   - Appointment reminders
   - Photo analysis for developmental milestones
   - Integration with health apps
   - Multi-language support
