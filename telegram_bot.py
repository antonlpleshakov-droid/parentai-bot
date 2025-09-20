"""
Telegram Bot for ParentAI - AI-powered parenting assistant
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, BOT_NAME
from ai_service import ParentAIService
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize AI service
ai_service = ParentAIService()

# User data storage (in production, use a database)
user_data = {}

class ParentAIBot:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up all bot handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("age", self.age_command))
        self.application.add_handler(CommandHandler("topics", self.topics_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user_id = update.effective_user.id
        user_data[user_id] = {
            'child_age_months': None,
            'context': '',
            'conversation_history': []
        }
        
        welcome_message = f"""
👋 Welcome to {BOT_NAME}!

I'm your AI-powered parenting assistant, here to help you with questions about your child aged 0-3 years old.

I provide evidence-based advice based on professional literature and pediatric best practices.

To get started:
1. Use /age to set your child's age
2. Ask me any parenting question
3. Use /topics to see common topics I can help with

What would you like to know about your little one? 🤱
        """
        
        keyboard = [
            [InlineKeyboardButton("Set Child's Age", callback_data="set_age")],
            [InlineKeyboardButton("Common Topics", callback_data="show_topics")],
            [InlineKeyboardButton("Quick Help", callback_data="quick_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """
📚 **How to use ParentAI:**

**Commands:**
/start - Start the bot and see welcome message
/age - Set your child's age for personalized advice
/topics - See common topics I can help with
/help - Show this help message

**Common Questions I Can Help With:**
• Why is my baby crying and what should I do?
• When should I take my child for medical checkups?
• What activities are appropriate for my child's age?
• Sleep issues and routines
• Feeding and nutrition advice
• Developmental milestones
• Safety concerns

**Tips:**
• Be specific about your child's age for better advice
• Ask follow-up questions if you need clarification
• I'm here 24/7 for your parenting questions!

Just type your question and I'll provide professional, evidence-based advice. 💕
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def age_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /age command to set child's age."""
        keyboard = [
            [InlineKeyboardButton("0-3 months", callback_data="age_1")],
            [InlineKeyboardButton("3-6 months", callback_data="age_4")],
            [InlineKeyboardButton("6-12 months", callback_data="age_8")],
            [InlineKeyboardButton("1-2 years", callback_data="age_15")],
            [InlineKeyboardButton("2-3 years", callback_data="age_30")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Please select your child's age group for personalized advice:",
            reply_markup=reply_markup
        )
    
    async def topics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /topics command."""
        topics_text = """
🎯 **Common Topics I Can Help With:**

**Crying & Comfort:**
• Why is my baby crying?
• How to soothe a fussy baby
• Sleep issues and routines

**Medical & Health:**
• When to see the doctor
• Vaccination schedules
• Common health concerns

**Development & Activities:**
• Age-appropriate activities
• Developmental milestones
• Learning and play ideas

**Feeding & Nutrition:**
• Breastfeeding support
• Introducing solids
• Picky eating solutions

**Safety & Behavior:**
• Childproofing your home
• Managing tantrums
• Positive discipline

Just ask me about any of these topics! 💬
        """
        await update.message.reply_text(topics_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Initialize user data if not exists
        if user_id not in user_data:
            user_data[user_id] = {
                'child_age_months': None,
                'context': '',
                'conversation_history': []
            }
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get AI response
        child_age = user_data[user_id]['child_age_months']
        user_context = user_data[user_id]['context']
        
        response = ai_service.generate_response(message_text, child_age, user_context)
        
        # Store conversation
        user_data[user_id]['conversation_history'].append({
            'question': message_text,
            'answer': response
        })
        
        # Send response
        await update.message.reply_text(response)
        
        # Add quick action buttons for common topics
        keyboard = [
            [InlineKeyboardButton("Why is my baby crying?", callback_data="quick_crying")],
            [InlineKeyboardButton("Medical checkups", callback_data="quick_medical")],
            [InlineKeyboardButton("Age activities", callback_data="quick_activities")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Need help with something else? Try these common topics:",
            reply_markup=reply_markup
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline keyboards."""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        data = query.data
        
        if data.startswith("age_"):
            # Handle age selection
            age_months = int(data.split("_")[1])
            user_data[user_id]['child_age_months'] = age_months
            
            age_groups = {
                1: "0-3 months",
                4: "3-6 months", 
                8: "6-12 months",
                15: "1-2 years",
                30: "2-3 years"
            }
            
            age_group = age_groups.get(age_months, "unknown")
            await query.edit_message_text(f"✅ Great! I've set your child's age to {age_group}. Now I can provide more personalized advice!")
        
        elif data == "set_age":
            await self.age_command(update, context)
        
        elif data == "show_topics":
            await self.topics_command(update, context)
        
        elif data == "quick_help":
            help_text = """
🚀 **Quick Help:**

**Most Common Questions:**
• "My baby won't stop crying, what should I do?"
• "How often should I take my child to the doctor?"
• "What activities can I do with my 1-year-old?"

**Just type your question naturally!** I understand questions like:
• "Baby crying help"
• "When doctor visit"
• "Activities for 6 months old"

I'm here to help! 💕
            """
            await query.edit_message_text(help_text)
        
        elif data == "quick_crying":
            response = ai_service.generate_response(
                "My baby is crying and I don't know what to do",
                user_data[user_id]['child_age_months']
            )
            await query.edit_message_text(response)
        
        elif data == "quick_medical":
            response = ai_service.generate_response(
                "When should I take my child for medical checkups?",
                user_data[user_id]['child_age_months']
            )
            await query.edit_message_text(response)
        
        elif data == "quick_activities":
            response = ai_service.generate_response(
                "What activities are appropriate for my child's age?",
                user_data[user_id]['child_age_months']
            )
            await query.edit_message_text(response)
    
    def run(self):
        """Start the bot."""
        logger.info(f"Starting {BOT_NAME}...")
        self.application.run_polling()

if __name__ == "__main__":
    bot = ParentAIBot()
    bot.run()
