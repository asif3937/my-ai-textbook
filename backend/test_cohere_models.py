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
        
        # List available models
        print("Listing available models...")
        models = client.models.list()
        print(f"Available models: {models}")
        
        # Filter for chat models
        chat_models = [model for model in models if 'command' in model.name.lower()]
        print(f"Available command models: {chat_models}")
        
        for model in chat_models:
            print(f"Model name: {model.name}, Endpoints: {getattr(model, 'endpoints', 'Unknown')}")
        
    except Exception as e:
        print(f"Cohere API error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("No Cohere API key available")