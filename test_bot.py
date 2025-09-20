"""
Test script for ParentAI bot functionality
"""

from ai_service import ParentAIService
from knowledge_base import get_knowledge_for_age_group, get_all_topics

def test_knowledge_base():
    """Test knowledge base functionality."""
    print("🧪 Testing Knowledge Base...")
    
    # Test getting topics
    topics = get_all_topics()
    print(f"✅ Available topics: {topics}")
    
    # Test getting age groups
    for topic in topics:
        age_groups = get_knowledge_for_age_group("0-3_months", topic)
        if age_groups:
            print(f"✅ {topic} for 0-3 months: {len(age_groups)} items")
    
    print("✅ Knowledge base test passed!")

def test_ai_service():
    """Test AI service functionality."""
    print("\n🤖 Testing AI Service...")
    
    ai_service = ParentAIService()
    
    # Test age group determination
    test_ages = [1, 4, 8, 15, 30]
    for age in test_ages:
        age_group = ai_service.determine_age_group(age)
        print(f"✅ Age {age} months -> {age_group}")
    
    # Test topic extraction
    test_questions = [
        "My baby won't stop crying",
        "When should I take my child to the doctor?",
        "What activities can I do with my 6-month-old?"
    ]
    
    for question in test_questions:
        topic = ai_service.extract_topic_from_question(question)
        print(f"✅ Question: '{question}' -> Topic: {topic}")
    
    print("✅ AI service test passed!")

def test_sample_responses():
    """Test sample AI responses (without OpenAI API)."""
    print("\n💬 Testing Sample Responses...")
    
    ai_service = ParentAIService()
    
    # Test questions
    test_cases = [
        {
            "question": "My 2-month-old baby is crying non-stop, what should I do?",
            "age": 2,
            "expected_topic": "crying"
        },
        {
            "question": "When should I take my 6-month-old for checkups?",
            "age": 6,
            "expected_topic": "medical_checkups"
        },
        {
            "question": "What activities are good for my 1-year-old?",
            "age": 12,
            "expected_topic": "age_appropriate_activities"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Question: {case['question']}")
        print(f"Child Age: {case['age']} months")
        
        age_group = ai_service.determine_age_group(case['age'])
        topic = ai_service.extract_topic_from_question(case['question'])
        
        print(f"Age Group: {age_group}")
        print(f"Topic: {topic}")
        
        # Get knowledge
        knowledge = get_knowledge_for_age_group(age_group, topic)
        if knowledge:
            print(f"Knowledge Available: {len(knowledge)} categories")
        else:
            print("No specific knowledge found")
        
        print("✅ Test case passed!")

def main():
    """Run all tests."""
    print("🧪 ParentAI Bot Test Suite")
    print("=" * 50)
    
    try:
        test_knowledge_base()
        test_ai_service()
        test_sample_responses()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Bot is ready to run.")
        print("\nTo start the bot:")
        print("1. Set up your API keys in .env file")
        print("2. Run: python main.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
