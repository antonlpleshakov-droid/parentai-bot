# 🚀 QUICK DEPLOY - ParentAI Bot

## **SUPER FAST DEPLOYMENT (2 minutes)**

### **Step 1: Get API Keys (30 seconds)**
1. **Telegram Bot Token:**
   - Go to [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot`
   - Name: `ParentAI Bot`
   - Username: `your_parentai_bot` (must be unique)
   - Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **OpenAI API Key:**
   - Go to [platform.openai.com](https://platform.openai.com)
   - Sign up/login
   - Go to API Keys → Create new key
   - Copy the key (starts with `sk-`)

### **Step 2: Deploy to Railway (90 seconds)**
1. **Go to [railway.app](https://railway.app)**
2. **Sign up with GitHub** (if you don't have GitHub, create account first)
3. **Click "New Project"**
4. **Click "Deploy from GitHub repo"**
5. **Create new repository:**
   - Repository name: `parentai-bot`
   - Make it public
   - Upload all files from this folder
6. **Connect Railway to your repo**
7. **Add Environment Variables:**
   - Click on your project
   - Go to "Variables" tab
   - Add: `TELEGRAM_BOT_TOKEN` = your bot token
   - Add: `OPENAI_API_KEY` = your OpenAI key
8. **Click "Deploy"**

### **Step 3: Test Your Bot (30 seconds)**
1. **Find your bot on Telegram** (search for the username you created)
2. **Send `/start`**
3. **Test with: "My baby is crying, what should I do?"**
4. **Set child's age with `/age`**

## **🎉 DONE! Your bot is live 24/7**

---

## **Alternative: Deploy to Heroku**

If you prefer Heroku:

1. **Install Heroku CLI** from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
2. **Run these commands:**
   ```bash
   heroku create your-parentai-bot
   heroku config:set TELEGRAM_BOT_TOKEN=your_token_here
   heroku config:set OPENAI_API_KEY=your_key_here
   git add .
   git commit -m "Deploy ParentAI Bot"
   git push heroku main
   ```

---

## **What You Get:**

✅ **AI-powered parenting assistant**  
✅ **24/7 availability**  
✅ **Professional advice based on literature**  
✅ **Age-specific guidance (0-3 years)**  
✅ **Quick action buttons**  
✅ **Context-aware responses**  

## **Cost:**
- **Railway**: Free tier available, then ~$5/month
- **OpenAI API**: ~$5-20/month depending on usage
- **Total**: ~$10-25/month

## **Need Help?**
- Railway has excellent documentation
- The bot is production-ready
- All code is optimized and tested
