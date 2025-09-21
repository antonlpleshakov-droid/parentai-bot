"""
Улучшенный AI сервис для генерации профессиональных советов по воспитанию
"""

from config import OPENAI_API_KEY
from book_rag_system import initialize_book_rag
import json
import logging

logger = logging.getLogger(__name__)

class EnhancedParentAIService:
    def __init__(self, book_path: str = None):
        """Инициализация улучшенного AI сервиса с RAG системой"""
        self.book_path = book_path
        self.rag_system = None
        self.fallback_responses = self._load_fallback_responses()
        
        # Инициализируем RAG систему если путь к книге указан
        if book_path:
            try:
                self.rag_system = initialize_book_rag(book_path, "book_embeddings.json")
                logger.info("RAG система успешно инициализирована")
            except Exception as e:
                logger.error(f"Ошибка инициализации RAG системы: {e}")
                self.rag_system = None
    
    def _load_fallback_responses(self):
        """Загружает fallback ответы для случаев, когда RAG система недоступна"""
        return {
            "crying_and_comfort": {
                "0-3_months": "Согласно принципам Петрановской, плач ребенка в этом возрасте - это способ общения, а не манипуляция. Немедленно подойдите к ребенку, возьмите на руки и проверьте физические потребности. Говорите ласково: 'Я здесь, мама рядом, все будет хорошо'.",
                "3-12_months": "Ребенок начинает понимать причинно-следственные связи. Подойдите спокойно, возьмите на руки и объясните: 'Мама здесь, все хорошо'. Для детей старше 6 месяцев: 'Я вижу, что тебе грустно'.",
                "1-3_years": "Ребенок может выражать эмоции словами. Присядьте на уровень ребенка, спросите: 'Расскажи, что случилось?' Обнимите и скажите: 'Я понимаю, что тебе грустно'."
            },
            "sleep_issues": {
                "0-3_months": "Сон - это навык, который нужно развивать. Создайте ритуал: купание → кормление → колыбельная. Укладывайте в одно и то же время, создайте спокойную атмосферу. Не переживайте, если ребенок засыпает на руках.",
                "3-12_months": "Ребенок начинает понимать последовательность действий. Сохраняйте ритуал: купание → книга → колыбельная. Укладывайте в кроватку, но оставайтесь рядом. Если просыпается - утешьте, но не вынимайте из кроватки.",
                "1-3_years": "Ребенок может сопротивляться сну из-за страха разлуки. Объясните: 'Сон нужен, чтобы расти и быть сильным'. Создайте ритуал: ужин → игра → книга → сон. Оставайтесь рядом, пока ребенок не заснет."
            },
            "discipline_and_boundaries": {
                "1-3_years": "Границы нужны, но они должны быть с любовью. Объясните правило: 'Нельзя бить маму, это больно'. Предложите альтернативу: 'Вместо этого можешь...' Если не слушается - остановите действие: 'Стоп, так нельзя'. Обнимите и объясните: 'Я люблю тебя, но это правило'."
            },
            "kindergarten_adaptation": {
                "2-3_years": "Адаптация к садику - это проверка привязанности. Начните подготовку заранее: рассказывайте о садике, играйте в 'садик' дома. Создайте ритуал прощания: объятия + поцелуй + 'Мама вернется'. Первые дни оставайтесь рядом, постепенно увеличивайте время."
            }
        }
    
    def determine_age_group(self, child_age_months):
        """Определяет возрастную группу на основе возраста в месяцах"""
        if child_age_months is None:
            return "1-3_years"
        elif child_age_months <= 3:
            return "0-3_months"
        elif child_age_months <= 12:
            return "3-12_months"
        else:
            return "1-3_years"
    
    def extract_topic_from_question(self, question):
        """Извлекает основную тему из вопроса пользователя"""
        question_lower = question.lower()
        
        # Расширенный список ключевых слов для тем Петрановской
        topic_keywords = {
            "crying_and_comfort": ["плач", "плачет", "кричит", "cry", "crying", "fuss", "fussy", "upset", "scream", "screaming", "успокоить", "утешить"],
            "sleep_issues": ["сон", "спит", "sleep", "спать", "засыпать", "просыпается", "уложить", "бессонница", "ночные пробуждения"],
            "discipline_and_boundaries": ["воспитание", "наказание", "границы", "discipline", "punishment", "boundaries", "истерика", "tantrum", "не слушается", "капризы"],
            "development_milestones": ["развитие", "развивается", "development", "milestone", "навыки", "skills", "говорит", "ходит", "ползает", "сидит"],
            "reading_interest": ["чтение", "читать", "книги", "reading", "books", "литература", "интерес к чтению", "любовь к книгам"],
            "kindergarten_adaptation": ["садик", "сад", "детский сад", "kindergarten", "адаптация", "не хочет в садик", "детский сад", "адаптация к садику"],
            "parenting_philosophy": ["воспитание", "родительство", "parenting", "привязанность", "attachment", "философия воспитания"],
            "attachment_theory": ["привязанность", "attachment", "любовь", "love", "близость", "closeness", "эмоциональная связь"],
            "feeding_nutrition": ["кормление", "еда", "питание", "feeding", "nutrition", "прикорм", "грудное вскармливание", "плохо ест"],
            "safety_behavior": ["безопасность", "safety", "поведение", "behavior", "травмы", "опасность", "ребенок в безопасности"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic
        
        return "parenting_philosophy"  # По умолчанию
    
    def generate_response(self, question, child_age_months=None, user_context=""):
        """Генерирует улучшенный AI ответ на основе контента книги"""
        try:
            # Определяем возрастную группу
            age_group = self.determine_age_group(child_age_months)
            topic = self.extract_topic_from_question(question)
            
            # Логируем запрос
            logger.info(f"Generating response for topic: {topic}, age_group: {age_group}")
            
            if self.rag_system:
                # Используем RAG систему для поиска релевантного контента из книги
                book_context = self.rag_system.get_context_for_question(question, max_chunks=3)
                
                if "не найдена релевантная информация" in book_context:
                    # Используем fallback ответ
                    return self._create_enhanced_fallback_response(question, age_group, topic)
                
                # Создаем контекст для AI с найденными фрагментами из книги
                context = self._create_enhanced_rag_context(question, age_group, book_context, user_context, topic)
                return self._call_openai_with_retry(context, question)
            else:
                # Fallback если RAG система не инициализирована
                return self._create_enhanced_fallback_response(question, age_group, topic)
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._create_error_response(question, age_group)
    
    def _create_enhanced_rag_context(self, question, age_group, book_context, user_context, topic):
        """Создает улучшенный контекст для AI на основе контента книги"""
        context = f"""
Вы - Petranovskaya AI, AI-бот, который отвечает на вопросы, связанные с развитием, воспитанием, здоровьем детей, а также на вопросах о родительстве. Ваш единственный источник информации - книга Людмилы Петрановской "Тайная опора".

ВОЗРАСТНАЯ ГРУППА: {age_group}
ТЕМА: {topic}
КОНТЕКСТ ПОЛЬЗОВАТЕЛЯ: {user_context}

РЕЛЕВАНТНЫЕ ФРАГМЕНТЫ ИЗ КНИГИ "ТАЙНАЯ ОПОРА":
{book_context}

СТРУКТУРА ОТВЕТА:
Отвечайте на том языке, на котором к вам обратились.
Тон ответов всегда дружелюбный и эмпатичный.

Давайте РАЗВЕРНУТЫЙ, ПОДРОБНЫЙ ответ на вопрос в следующем формате:

1. ПОНИМАНИЕ ПРОБЛЕМЫ (2-3 предложения):
   - Покажите, что вы понимаете ситуацию родителя
   - Объясните, почему это происходит с точки зрения развития ребенка
   - Проявите эмпатию к сложности ситуации

2. КРАТКИЙ ОТВЕТ (1-2 предложения):
   - Суть решения проблемы
   - Основной принцип из теории привязанности

3. ПОДРОБНОЕ РЕШЕНИЕ (минимум 5-7 пунктов):
   - Конкретные пошаговые действия
   - Для каждого действия: ЧТО делать, КАК делать, КОГДА делать
   - Конкретные фразы для разговора с ребенком
   - Примеры ситуаций и реакций
   - Что делать, если не помогает
   - Альтернативные подходы

4. ПРАКТИЧЕСКИЕ ПРИМЕРЫ:
   - Реальные ситуации из жизни
   - Диалоги с ребенком
   - Примеры игр, занятий, ритуалов
   - Конкретные фразы и выражения

5. ЧТО НЕ ДЕЛАТЬ (2-3 пункта):
   - Частые ошибки родителей
   - Чего избегать
   - Почему это не работает

6. ДОПОЛНИТЕЛЬНЫЕ СОВЕТЫ:
   - Как подготовиться к ситуации
   - Как предотвратить проблему в будущем
   - Когда обращаться к специалисту
   - Долгосрочные стратегии

7. ИСТОЧНИКИ И ДОПОЛНИТЕЛЬНОЕ ЧТЕНИЕ:
   - Конкретные главы из книги "Тайная опора"
   - Дополнительные темы для изучения
   - Связанные принципы теории привязанности

8. ПОДДЕРЖКА И ПРОДОЛЖЕНИЕ:
   - Эмпатичная фраза поддержки
   - Предложение дальнейшей помощи
   - Ободряющие слова для родителей

ОБЯЗАТЕЛЬНО:
- Минимум 400-600 слов в ответе
- Конкретные примеры и фразы
- Практические советы, которые можно применить СЕГОДНЯ
- Учет возраста ребенка
- Эмпатия и понимание сложности ситуации
- ОСНОВЫВАЙТЕСЬ ТОЛЬКО НА НАЙДЕННЫХ ФРАГМЕНТАХ ИЗ КНИГИ
- Используйте принципы теории привязанности
- Давайте надежду и поддержку родителям

ВОПРОС ПОЛЬЗОВАТЕЛЯ: {question}
"""
        return context
    
    def _create_enhanced_fallback_response(self, question, age_group, topic):
        """Создает улучшенный fallback ответ когда RAG система недоступна"""
        fallback_text = self.fallback_responses.get(topic, {}).get(age_group, "")
        
        if not fallback_text:
            fallback_text = f"""Согласно принципам из книги Людмилы Петрановской "Тайная опора":

**Понимание проблемы:** Я понимаю, что вы столкнулись с ситуацией, которая требует внимания и заботы. Это нормально - воспитание детей - это сложный процесс, требующий терпения и понимания.

**Краткий ответ:** Основной принцип - это любовь, принятие и понимание потребностей ребенка. Ребенок - это личность, а не проект для воспитания.

**Что делать:**
1. Оставайтесь спокойными и уверенными
2. Покажите ребенку, что вы его понимаете
3. Объясните ситуацию простыми словами
4. Предложите решение вместе
5. Обнимите и поддержите

**Что НЕ делать:**
- Не наказывайте отказом в любви
- Не игнорируйте эмоции ребенка
- Не сравнивайте с другими детьми

**Источники:** Книга "Тайная опора" Людмилы Петрановской

**Поддержка:** Помните, что вы - хороший родитель, и ваша любовь - это самое важное для ребенка.

Чем еще могу помочь?"""
        
        return f"""Извините, но я не могу найти релевантную информацию в книге "Тайная опора" для ответа на ваш вопрос.

Вопрос: {question}
Возрастная группа: {age_group}

{fallback_text}

Возможные причины:
- Вопрос не связан с темами воспитания детей
- В книге нет информации по этой конкретной теме
- RAG система не инициализирована

Попробуйте переформулировать вопрос или обратитесь к другим темам:
• Плач и утешение детей
• Проблемы со сном
• Дисциплина и установление границ
• Развитие ребенка по возрастам
• Формирование привязанности

Чем еще могу помочь?"""
    
    def _create_error_response(self, question, age_group):
        """Создает ответ при ошибке"""
        return f"""Извините, произошла техническая ошибка при генерации ответа.

Вопрос: {question}
Возрастная группа: {age_group}

Пожалуйста, попробуйте:
1. Переформулировать вопрос
2. Обратиться к другим темам
3. Попробовать позже

Я специализируюсь на вопросах развития, воспитания, здоровья детей и родительства на основе книги Людмилы Петрановской "Тайная опора".

Чем еще могу помочь?"""
    
    def _call_openai_with_retry(self, context, question, max_retries=3):
        """Вызывает OpenAI API с повторными попытками"""
        for attempt in range(max_retries):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": context},
                        {"role": "user", "content": question}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                logger.warning(f"OpenAI API call attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    return self._create_error_response(question, "unknown")
                continue
        
        return self._create_error_response(question, "unknown")
    
    def get_user_insights(self, user_id, user_data):
        """Получает инсайты о пользователе на основе его данных"""
        if user_id not in user_data:
            return "Нет данных о пользователе"
        
        user_info = user_data[user_id]
        total_questions = user_info.get('total_questions', 0)
        favorite_topics = user_info.get('favorite_topics', [])
        child_age = user_info.get('child_age_months')
        
        insights = []
        
        if total_questions > 0:
            insights.append(f"Вы задали {total_questions} вопросов")
        
        if favorite_topics:
            topic_names = {
                "crying_and_comfort": "Плач и утешение",
                "sleep_issues": "Проблемы со сном",
                "discipline_and_boundaries": "Дисциплина и границы",
                "development_milestones": "Развитие ребенка",
                "kindergarten_adaptation": "Адаптация к садику"
            }
            topic_display = [topic_names.get(topic, topic) for topic in favorite_topics[:3]]
            insights.append(f"Ваши любимые темы: {', '.join(topic_display)}")
        
        if child_age:
            age_groups = {
                1: "0-3 месяца",
                4: "3-6 месяцев", 
                8: "6-12 месяцев",
                15: "1-2 года",
                30: "2-3 года"
            }
            age_group = age_groups.get(child_age, "неизвестно")
            insights.append(f"Возраст ребенка: {age_group}")
        
        return "; ".join(insights) if insights else "Нет данных для анализа"
