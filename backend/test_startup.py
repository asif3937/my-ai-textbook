import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the main app to check if it loads without errors
    from main import app
    print("+ Main app imported successfully")

    # Test creating the services
    from services.generation_service import GenerationService
    from services.embedding_service import EmbeddingService
    from services.retrieval_service import RetrievalService

    print("+ All services imported successfully")

    # Try to create instances
    gen_service = GenerationService()
    emb_service = EmbeddingService()
    retrieval_service = RetrievalService()

    print("+ All services instantiated successfully")
    print(f"Generation service fallback mode: {getattr(gen_service, 'fallback_mode', 'N/A')}")
    print(f"Embedding service fallback mode: {getattr(emb_service, 'fallback_mode', 'N/A')}")

    print("\nApplication should be able to start successfully with fallback services.")
    print("The system will work but with limited functionality due to missing local models.")

except Exception as e:
    print(f"- Error: {e}")
    import traceback
    traceback.print_exc()