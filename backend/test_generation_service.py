#!/usr/bin/env python
"""
Test script to verify the generation service initialization
"""
from services.generation_service import GenerationService
from config.settings import settings

def test_generation_service():
    print("Testing Generation Service initialization...")
    print(f"Language Model Provider: {settings.LANGUAGE_MODEL_PROVIDER}")
    print(f"Cohere API Key available: {bool(settings.COHERE_API_KEY)}")
    print(f"OpenAI API Key available: {bool(settings.OPENAI_API_KEY)}")
    
    try:
        # Initialize the generation service
        gen_service = GenerationService()
        
        print(f"Generation service initialized successfully!")
        print(f"Using local model: {getattr(gen_service, 'use_local', 'Unknown')}")
        print(f"Model: {getattr(gen_service, 'model', 'Unknown')}")
        print(f"In fallback mode: {getattr(gen_service, 'fallback_mode', False)}")
        
        # Test a simple generation
        test_context = [
            {
                "text": "Machine learning is a method of data analysis that automates analytical model building.",
                "metadata": {"chapter": 1, "page": 1}
            }
        ]
        
        result = gen_service.generate_answer(
            query="What is machine learning?",
            context=test_context,
            mode="full_book"
        )
        
        print(f"\nTest generation result:")
        print(f"Answer: {result['answer'][:100]}...")
        print(f"Citations: {len(result['citations'])}")
        print(f"Model used: {result['model']}")
        
        return True
        
    except Exception as e:
        print(f"Error initializing generation service: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Generation Service Test")
    print("=" * 30)
    
    success = test_generation_service()
    
    print("\n" + "=" * 30)
    if success:
        print("Generation service is working properly!")
    else:
        print("Generation service needs to be fixed.")