import os
# Unset the environment variable to force reading from .env file
if 'QDRANT_API_KEY' in os.environ:
    del os.environ['QDRANT_API_KEY']

from config.settings import settings
import cohere

print(f"COHERE_API_KEY available: {bool(settings.COHERE_API_KEY)}")

if settings.COHERE_API_KEY:
    try:
        print("Testing Cohere connection...")
        client = cohere.Client(settings.COHERE_API_KEY)
        
        # Test embedding
        print("Testing embeddings...")
        response = client.embed(
            texts=["Hello world"],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        print(f"Embedding test successful. Embedding length: {len(response.embeddings[0])}")
        
        # Test generation
        print("Testing generation...")
        response = client.chat(
            message="Hello, how are you?",
            model="command",
            temperature=0.3,
            max_tokens=50,
        )
        print(f"Generation test successful. Response: {response.text[:50]}...")
        
        print("Cohere API is working correctly!")
    except Exception as e:
        print(f"Cohere API error: {e}")
else:
    print("No Cohere API key available")