import os
os.environ['QDRANT_API_KEY'] = ''
os.environ['COHERE_API_KEY'] = ''

from services.generation_service import GenerationService

print("Testing GenerationService with no API keys (should use local model)...")

try:
    gen_service = GenerationService()
    print(f"Generation service initialized. Using local: {gen_service.use_local}")
    print(f"Fallback mode: {getattr(gen_service, 'fallback_mode', False)}")

    if getattr(gen_service, 'fallback_mode', False):
        print("Using fallback mode.")
        # Test a simple generation
        result = gen_service.generate_answer(
            query="Hello, how are you?",
            context=[{"text": "This is a test context", "metadata": {}, "relevance_score": 1.0}]
        )
        print("Generation successful!")
        print(f"Answer: {result['answer'][:200]}...")
    else:
        print("Not using fallback mode")
        # Test a simple generation
        result = gen_service.generate_answer(
            query="Hello, how are you?",
            context=[{"text": "This is a test context", "metadata": {}, "relevance_score": 1.0}]
        )
        print("Generation successful!")
        print(f"Answer: {result['answer'][:100]}...")
        
except Exception as e:
    print(f"Error initializing GenerationService: {e}")
    import traceback
    traceback.print_exc()