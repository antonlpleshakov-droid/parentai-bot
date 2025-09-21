"""
Улучшенный Telegram Bot для ParentAI с дополнительными функциями
"""

import logging
import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, BOT_NAME
from ai_service import ParentAIService

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize AI service with RAG system
BOOK_PATH = "Петрановская_Тайная опора.pdf"
ai_service = ParentAIService(book_path=BOOK_PATH)

# User data storage with enhanced features
user_data = {}

class EnhancedParentAIBot:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
        self.load_user_data()
    
    def load_user_data(self):
        """Load user data from file if exists"""
        try:
            if os.path.exists('user_data.json'):
                with open('user_data.json', 'r', encoding='utf-8') as f:
                    global user_data
                    user_data = json.load(f)
                logger.info(f"Loaded user data for {len(user_data)} users")
        except Exception as e:
            logger.error(f"Error loading user data: {e}")
    
    def save_user_data(self):
        """Save user data to file"""
        try:
            with open('user_data.json', 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=2)
            logger.info("User data saved successfully")
        except Exception as e:
            logger.error(f"Error saving user data: {e}")
    
    def setup_handlers(self):
        """Set up all bot handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("age", self.age_command))
        self.application.add_handler(CommandHandler("topics", self.topics_command))
        self.application.add_handler(CommandHandler("history", self.history_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("profile", self.profile_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "Пользователь"
        
        # Initialize user data if not exists
        if user_id not in user_data:
            user_data[user_id] = {
                'name': user_name,
                'child_age_months': None,
                'context': '',
                'conversation_history': [],
                'total_questions': 0,
                'favorite_topics': [],
                'registration_date': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat()
            }
            self.save_user_data()
        
        # Update last activity
        user_data[user_id]['last_activity'] = datetime.now().isoformat()
        
        welcome_message = f"""
👋 Добро пожаловать в {BOT_NAME}, {user_name}!

Я ваш помощник по воспитанию детей, основанный исключительно на книге Людмилы Петрановской "Тайная опора".

Я даю советы, основанные на теории привязанности и принципах, описанных в этой замечательной книге.

**Новые возможности:**
📚 История ваших диалогов
📊 Статистика использования
👤 Персональный профиль
🎯 Рекомендации по темам

Чтобы начать:
1. Используйте /age чтобы указать возраст вашего ребенка
2. Задайте мне любой вопрос о воспитании
3. Используйте /topics чтобы увидеть основные темы
4. Используйте /history чтобы посмотреть историю диалогов

Что бы вы хотели узнать о вашем малыше? 🤱
        """
        
        keyboard = [
            [InlineKeyboardButton("Указать возраст ребенка", callback_data="set_age")],
            [InlineKeyboardButton("Основные темы", callback_data="show_topics")],
            [InlineKeyboardButton("История диалогов", callback_data="show_history")],
            [InlineKeyboardButton("Мой профиль", callback_data="show_profile")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """
📚 **Как использовать ParentAI:**

**Основные команды:**
/start - Начать работу с ботом
/age - Указать возраст ребенка для персонализированных советов
/topics - Посмотреть основные темы, с которыми я могу помочь
/history - Посмотреть историю ваших диалогов
/stats - Посмотреть статистику использования
/profile - Посмотреть ваш профиль
/help - Показать эту справку

**Частые вопросы, с которыми я могу помочь:**
• Почему мой ребенок плачет и что делать?
• Когда нужно обращаться к врачу?
• Какие занятия подходят для возраста моего ребенка?
• Проблемы со сном и режимом
• Советы по кормлению и питанию
• Этапы развития ребенка
• Вопросы безопасности
• Адаптация к детскому саду
• Формирование привязанности

**Советы:**
• Укажите возраст ребенка для более точных советов
• Задавайте уточняющие вопросы, если нужно
• Я работаю 24/7 для ваших вопросов о воспитании!
• Используйте /history чтобы вернуться к предыдущим советам

Просто напишите свой вопрос, и я дам профессиональный, основанный на принципах Петрановской совет. 💕
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def age_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /age command to set child's age."""
        keyboard = [
            [InlineKeyboardButton("0-3 месяца", callback_data="age_1")],
            [InlineKeyboardButton("3-6 месяцев", callback_data="age_4")],
            [InlineKeyboardButton("6-12 месяцев", callback_data="age_8")],
            [InlineKeyboardButton("1-2 года", callback_data="age_15")],
            [InlineKeyboardButton("2-3 года", callback_data="age_30")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Пожалуйста, выберите возрастную группу вашего ребенка для персонализированных советов:",
            reply_markup=reply_markup
        )
    
    async def topics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /topics command."""
        topics_text = """
🎯 **Основные темы, с которыми я могу помочь:**

**Плач и утешение:**
• Почему ребенок плачет?
• Как успокоить капризного малыша
• Проблемы со сном и режимом

**Медицина и здоровье:**
• Когда обращаться к врачу
• График прививок
• Частые проблемы со здоровьем

**Развитие и занятия:**
• Занятия, подходящие по возрасту
• Этапы развития
• Идеи для игр и обучения

**Кормление и питание:**
• Поддержка грудного вскармливания
• Введение прикорма
• Решение проблем с едой

**Безопасность и поведение:**
• Безопасность дома
• Управление истериками
• Позитивная дисциплина

**Адаптация и социализация:**
• Адаптация к детскому саду
• Формирование привязанности
• Развитие социальных навыков

Просто спросите меня о любой из этих тем! 💬
        """
        await update.message.reply_text(topics_text, parse_mode='Markdown')
    
    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /history command."""
        user_id = update.effective_user.id
        
        if user_id not in user_data or not user_data[user_id]['conversation_history']:
            await update.message.reply_text("У вас пока нет истории диалогов. Начните задавать вопросы!")
            return
        
        history = user_data[user_id]['conversation_history']
        
        if len(history) <= 5:
            # Show all history if 5 or fewer items
            history_text = "📚 **Ваша история диалогов:**\n\n"
            for i, item in enumerate(history, 1):
                history_text += f"**{i}.** {item['question'][:50]}...\n"
                history_text += f"   *{item['answer'][:100]}...*\n\n"
        else:
            # Show last 5 items
            history_text = "📚 **Последние 5 диалогов:**\n\n"
            for i, item in enumerate(history[-5:], 1):
                history_text += f"**{i}.** {item['question'][:50]}...\n"
                history_text += f"   *{item['answer'][:100]}...*\n\n"
        
        history_text += f"Всего диалогов: {len(history)}"
        
        await update.message.reply_text(history_text, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command."""
        user_id = update.effective_user.id
        
        if user_id not in user_data:
            await update.message.reply_text("Сначала начните диалог с ботом!")
            return
        
        user_info = user_data[user_id]
        total_questions = user_info.get('total_questions', 0)
        registration_date = user_info.get('registration_date', 'Неизвестно')
        last_activity = user_info.get('last_activity', 'Неизвестно')
        child_age = user_info.get('child_age_months')
        
        age_text = "Не указан"
        if child_age:
            age_groups = {
                1: "0-3 месяца",
                4: "3-6 месяцев", 
                8: "6-12 месяцев",
                15: "1-2 года",
                30: "2-3 года"
            }
            age_text = age_groups.get(child_age, "Неизвестно")
        
        stats_text = f"""
📊 **Ваша статистика:**

👤 **Профиль:**
• Имя: {user_info.get('name', 'Не указано')}
• Возраст ребенка: {age_text}
• Дата регистрации: {registration_date[:10] if registration_date != 'Неизвестно' else 'Неизвестно'}

📈 **Активность:**
• Всего вопросов: {total_questions}
• Последняя активность: {last_activity[:16] if last_activity != 'Неизвестно' else 'Неизвестно'}

🎯 **Популярные темы:**
{', '.join(user_info.get('favorite_topics', ['Пока нет данных']))}

💡 **Совет:** Используйте /age чтобы указать возраст ребенка для более точных советов!
        """
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command."""
        user_id = update.effective_user.id
        
        if user_id not in user_data:
            await update.message.reply_text("Сначала начните диалог с ботом!")
            return
        
        user_info = user_data[user_id]
        
        keyboard = [
            [InlineKeyboardButton("Изменить возраст ребенка", callback_data="set_age")],
            [InlineKeyboardButton("Очистить историю", callback_data="clear_history")],
            [InlineKeyboardButton("Назад", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        profile_text = f"""
👤 **Ваш профиль:**

**Основная информация:**
• Имя: {user_info.get('name', 'Не указано')}
• Возраст ребенка: {user_info.get('child_age_months', 'Не указан')} месяцев
• Дата регистрации: {user_info.get('registration_date', 'Неизвестно')[:10]}

**Статистика:**
• Всего вопросов: {user_info.get('total_questions', 0)}
• Последняя активность: {user_info.get('last_activity', 'Неизвестно')[:16]}

**Настройки:**
Используйте кнопки ниже для изменения настроек.
        """
        
        await update.message.reply_text(profile_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Initialize user data if not exists
        if user_id not in user_data:
            user_data[user_id] = {
                'name': update.effective_user.first_name or "Пользователь",
                'child_age_months': None,
                'context': '',
                'conversation_history': [],
                'total_questions': 0,
                'favorite_topics': [],
                'registration_date': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat()
            }
        
        # Update user activity
        user_data[user_id]['last_activity'] = datetime.now().isoformat()
        user_data[user_id]['total_questions'] += 1
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get AI response
        child_age = user_data[user_id]['child_age_months']
        user_context = user_data[user_id]['context']
        
        response = ai_service.generate_response(message_text, child_age, user_context)
        
        # Store conversation
        conversation_item = {
            'question': message_text,
            'answer': response,
            'timestamp': datetime.now().isoformat(),
            'child_age': child_age
        }
        user_data[user_id]['conversation_history'].append(conversation_item)
        
        # Update favorite topics
        topic = ai_service.extract_topic_from_question(message_text)
        if topic not in user_data[user_id]['favorite_topics']:
            user_data[user_id]['favorite_topics'].append(topic)
        
        # Save user data
        self.save_user_data()
        
        # Send response
        await update.message.reply_text(response)
        
        # Add quick action buttons for common topics
        keyboard = [
            [InlineKeyboardButton("Почему ребенок плачет?", callback_data="quick_crying")],
            [InlineKeyboardButton("Проблемы со сном", callback_data="quick_sleep")],
            [InlineKeyboardButton("Занятия по возрасту", callback_data="quick_activities")],
            [InlineKeyboardButton("История диалогов", callback_data="show_history")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Нужна помощь с чем-то еще? Попробуйте эти частые темы:",
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
                1: "0-3 месяца",
                4: "3-6 месяцев", 
                8: "6-12 месяцев",
                15: "1-2 года",
                30: "2-3 года"
            }
            
            age_group = age_groups.get(age_months, "неизвестно")
            await query.edit_message_text(f"✅ Отлично! Я установил возраст вашего ребенка как {age_group}. Теперь я могу давать более персонализированные советы!")
        
        elif data == "set_age":
            await self.age_command(update, context)
        
        elif data == "show_topics":
            await self.topics_command(update, context)
        
        elif data == "show_history":
            await self.history_command(update, context)
        
        elif data == "show_profile":
            await self.profile_command(update, context)
        
        elif data == "quick_crying":
            response = ai_service.generate_response(
                "Мой ребенок плачет и я не знаю что делать",
                user_data[user_id]['child_age_months']
            )
            await query.edit_message_text(response)
        
        elif data == "quick_sleep":
            response = ai_service.generate_response(
                "Как уложить ребенка спать?",
                user_data[user_id]['child_age_months']
            )
            await query.edit_message_text(response)
        
        elif data == "quick_activities":
            response = ai_service.generate_response(
                "Какие занятия подходят для возраста моего ребенка?",
                user_data[user_id]['child_age_months']
            )
            await query.edit_message_text(response)
        
        elif data == "clear_history":
            user_data[user_id]['conversation_history'] = []
            self.save_user_data()
            await query.edit_message_text("✅ История диалогов очищена!")
        
        elif data == "back_to_main":
            await query.edit_message_text("Главное меню. Используйте /start для начала работы.")
    
    def run(self):
        """Start the bot."""
        logger.info(f"Starting {BOT_NAME}...")
        self.application.run_polling()

if __name__ == "__main__":
    bot = EnhancedParentAIBot()
    bot.run()
