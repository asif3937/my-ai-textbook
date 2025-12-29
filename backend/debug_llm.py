import sys
import os
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Starting LLM debug...")

# Print environment variables directly
print(f"Direct env LANGUAGE_MODEL_PROVIDER: {os.getenv('LANGUAGE_MODEL_PROVIDER', 'Not set')}")
print(f"Direct env COHERE_API_KEY: {bool(os.getenv('COHERE_API_KEY', ''))}")
print(f"Direct env OPENAI_API_KEY: {bool(os.getenv('OPENAI_API_KEY', ''))}")

# Import settings first
from config.settings import settings
print(f"Settings LANGUAGE_MODEL_PROVIDER: {settings.LANGUAGE_MODEL_PROVIDER}")
print(f"Settings COHERE_API_KEY is set: {bool(settings.COHERE_API_KEY)}")
print(f"Settings OPENAI_API_KEY is set: {bool(settings.OPENAI_API_KEY)}")

# Test embedding service initialization
print("\nTesting EmbeddingService initialization...")
try:
    from services.embedding_service import EmbeddingService
    embedding_service = EmbeddingService()
    print("EmbeddingService initialized successfully")
    print(f"Using local embeddings: {embedding_service.use_local}")
    if hasattr(embedding_service, 'fallback_mode'):
        print(f"Fallback mode: {embedding_service.fallback_mode}")
except Exception as e:
    print(f"Error initializing EmbeddingService: {e}")
    import traceback
    traceback.print_exc()

# Test generation service initialization
print("\nTesting GenerationService initialization...")
try:
    from services.generation_service import GenerationService
    generation_service = GenerationService()
    print("GenerationService initialized successfully")
    print(f"Using local LLM: {generation_service.use_local}")
    if hasattr(generation_service, 'fallback_mode'):
        print(f"Fallback mode: {generation_service.fallback_mode}")
except Exception as e:
    print(f"Error initializing GenerationService: {e}")
    import traceback
    traceback.print_exc()

# Test retrieval service initialization
print("\nTesting RetrievalService initialization...")
try:
    from services.retrieval_service import RetrievalService
    retrieval_service = RetrievalService()
    print("RetrievalService initialized successfully")
except Exception as e:
    print(f"Error initializing RetrievalService: {e}")
    import traceback
    traceback.print_exc()

print("\nDebug completed.")