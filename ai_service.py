"""
AI service for generating professional parenting advice based on knowledge base.
"""

from config import OPENAI_API_KEY
from petranovskaya_knowledge_base import get_petranovskaya_advice, format_petranovskaya_response, get_all_petranovskaya_topics
import json

class ParentAIService:
    def __init__(self):
        self.knowledge_base_topics = get_all_petranovskaya_topics()
    
    def determine_age_group(self, child_age_months):
        """Determine age group based on child's age in months."""
        if child_age_months <= 3:
            return "0-3_months"
        elif child_age_months <= 6:
            return "3-6_months"
        elif child_age_months <= 12:
            return "6-12_months"
        else:
            return "1-3_years"
    
    def extract_topic_from_question(self, question):
        """Extract the main topic from user's question."""
        question_lower = question.lower()
        
        # Map keywords to Петрановская's topics
        topic_keywords = {
            "crying_and_comfort": ["плач", "плачет", "кричит", "cry", "crying", "fuss", "fussy", "upset", "scream", "screaming"],
            "sleep_issues": ["сон", "спит", "sleep", "спать", "засыпать", "просыпается"],
            "discipline_and_boundaries": ["воспитание", "наказание", "границы", "discipline", "punishment", "boundaries", "истерика", "tantrum"],
            "development_milestones": ["развитие", "развивается", "development", "milestone", "навыки", "skills"],
            "parenting_philosophy": ["воспитание", "родительство", "parenting", "привязанность", "attachment"],
            "attachment_theory": ["привязанность", "attachment", "любовь", "love", "близость", "closeness"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic
        
        return "parenting_philosophy"  # Default to general parenting philosophy
    
    def generate_response(self, question, child_age_months=None, user_context=""):
        """Generate AI response based on Петрановская's book only."""
        try:
            # Determine age group
            age_group = self.determine_age_group(child_age_months) if child_age_months else "1-3_years"
            
            # Extract topic
            topic = self.extract_topic_from_question(question)
            
            # Get Петрановская's advice
            petranovskaya_advice = get_petranovskaya_advice(topic, age_group)
            
            if not petranovskaya_advice:
                # Try without age group
                petranovskaya_advice = get_petranovskaya_advice(topic)
            
            if petranovskaya_advice:
                # Use Петрановская's knowledge directly
                return format_petranovskaya_response(topic, age_group)
            else:
                # Create context for AI based on Петрановская's principles
                context = self._create_petranovskaya_context(question, age_group, topic, user_context)
                
                # Generate response using OpenAI with Петрановская's context
                response = self._call_openai(context, question)
                
                return response
            
        except Exception as e:
            return f"Извините, у меня возникли проблемы с обработкой вашего вопроса. Попробуйте еще раз. Ошибка: {str(e)}"
    
    def _create_context(self, question, age_group, topic, knowledge, user_context):
        """Create context for AI based on knowledge base and user input."""
        context = f"""
You are ParentAI, a professional AI assistant specializing in parenting advice for children aged 0-3 years old. 
You provide evidence-based advice based on professional literature and pediatric best practices.

CHILD'S AGE GROUP: {age_group}
TOPIC: {topic}
USER CONTEXT: {user_context}

PROFESSIONAL KNOWLEDGE BASE:
"""
        
        if knowledge:
            context += f"\n{topic.upper()} GUIDANCE FOR {age_group.replace('_', ' ').upper()}:\n"
            for key, value in knowledge.items():
                if isinstance(value, list):
                    context += f"\n{key.replace('_', ' ').title()}:\n"
                    for item in value:
                        context += f"- {item}\n"
                else:
                    context += f"\n{key.replace('_', ' ').title()}: {value}\n"
        
        context += f"""

INSTRUCTIONS:
1. Provide professional, evidence-based advice based on the knowledge base above
2. Be empathetic and understanding of the parent's concerns
3. Give practical, actionable steps
4. Always prioritize child safety
5. When appropriate, suggest consulting a pediatrician
6. Keep responses concise but comprehensive
7. Use a warm, supportive tone
8. If the question is outside your expertise, acknowledge limitations and suggest professional consultation

USER QUESTION: {question}
"""
        
        return context
    
    def _create_petranovskaya_context(self, question, age_group, topic, user_context):
        """Create context for AI based on Петрановская's book only."""
        context = f"""
Вы - ParentAI, помощник по воспитанию детей, основанный исключительно на книге Людмилы Петрановской "Тайная опора".

ВОЗРАСТНАЯ ГРУППА: {age_group}
ТЕМА: {topic}
КОНТЕКСТ ПОЛЬЗОВАТЕЛЯ: {user_context}

ОСНОВЫ ИЗ КНИГИ "ТАЙНАЯ ОПОРА":

1. ТЕОРИЯ ПРИВЯЗАННОСТИ:
- Привязанность - это биологическая потребность ребенка, как еда и сон
- Безопасная привязанность дает ребенку уверенность в мире
- Привязанность формируется в первые годы жизни

2. ОСНОВНЫЕ ПРИНЦИПЫ:
- Ребенок - это личность, а не проект для воспитания
- Любовь и принятие - основа всего
- Доверие к ребенку и к себе
- Гибкость важнее строгих правил

3. ПОДХОД К ВОСПИТАНИЮ:
- Границы нужны, но они должны быть с любовью
- Ребенок проверяет границы, чтобы убедиться в прочности привязанности
- Наказание должно быть справедливым и понятным
- Никогда не наказывайте отказом в любви

4. ЧАСТЫЕ ОШИБКИ:
- Игнорирование плача "чтобы не избаловать"
- Попытки "воспитать" через наказания
- Сравнение с другими детьми
- Фокус на поведении, а не на отношениях

ИНСТРУКЦИИ:
1. Отвечайте ТОЛЬКО на основе принципов из книги "Тайная опора"
2. Если в книге нет информации по вопросу, честно скажите об этом
3. Всегда упоминайте, что совет основан на книге Петрановской
4. Используйте теплый, понимающий тон
5. Фокусируйтесь на отношениях, а не на поведении
6. Подчеркивайте важность привязанности и любви

ВОПРОС ПОЛЬЗОВАТЕЛЯ: {question}
"""
        return context
    
    def _call_openai(self, context, question):
        """Call OpenAI API to generate response."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"I apologize, but I'm having trouble accessing my AI capabilities right now. Please try again later. Error: {str(e)}"
    
    def get_quick_responses(self, topic, age_group):
        """Get quick response options for common topics."""
        knowledge = get_knowledge_for_age_group(age_group, topic)
        
        if not knowledge:
            return []
        
        quick_responses = []
        
        if topic == "crying":
            if "common_causes" in knowledge:
                quick_responses.extend(knowledge["common_causes"][:3])  # Top 3 causes
        
        elif topic == "medical_checkups":
            if "schedule" in knowledge:
                quick_responses.extend(knowledge["schedule"][:2])  # Next 2 appointments
        
        elif topic == "age_appropriate_activities":
            if "motor_skills" in knowledge:
                quick_responses.extend(knowledge["motor_skills"][:3])  # Top 3 activities
        
        return quick_responses
