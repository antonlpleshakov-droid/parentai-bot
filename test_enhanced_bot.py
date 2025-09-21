"""
Тестирование улучшенного бота
"""

from enhanced_ai_service import EnhancedParentAIService

def test_enhanced_ai_service():
    """Тестирует улучшенный AI сервис"""
    print("🤖 Тестирование улучшенного AI сервиса...")
    
    # Инициализируем сервис
    ai_service = EnhancedParentAIService()
    
    # Тестовые вопросы
    test_questions = [
        {
            "question": "Мой ребенок плачет и я не знаю что делать",
            "age": 6,
            "description": "Плач ребенка 6 месяцев"
        },
        {
            "question": "Как уложить ребенка спать?",
            "age": 18,
            "description": "Проблемы со сном 1.5 года"
        },
        {
            "question": "Ребенок не слушается, как наказывать?",
            "age": 24,
            "description": "Дисциплина 2 года"
        },
        {
            "question": "Что делать, если ребенок не хочет в садик?",
            "age": 30,
            "description": "Адаптация к садику 2.5 года"
        },
        {
            "question": "Как привить ребенку любовь к чтению?",
            "age": 20,
            "description": "Интерес к чтению 1.5 года"
        }
    ]
    
    for i, test in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"ТЕСТ {i}: {test['description']}")
        print(f"Вопрос: {test['question']}")
        print(f"Возраст: {test['age']} месяцев")
        print(f"{'='*60}")
        
        try:
            response = ai_service.generate_response(
                test['question'], 
                test['age']
            )
            print(f"Ответ:\n{response}")
        except Exception as e:
            print(f"Ошибка: {e}")
        
        print(f"\n{'-'*60}")

def test_topic_extraction():
    """Тестирует извлечение тем из вопросов"""
    print("\n🎯 Тестирование извлечения тем...")
    
    ai_service = EnhancedParentAIService()
    
    test_questions = [
        "Мой ребенок плачет",
        "Как уложить спать?",
        "Ребенок не слушается",
        "Не хочет в садик",
        "Как привить любовь к книгам?",
        "Плохо ест",
        "Безопасность дома"
    ]
    
    for question in test_questions:
        topic = ai_service.extract_topic_from_question(question)
        print(f"Вопрос: '{question}' -> Тема: {topic}")

if __name__ == "__main__":
    test_enhanced_ai_service()
    test_topic_extraction()
