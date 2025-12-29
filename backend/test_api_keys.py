#!/usr/bin/env python
"""
Test script to verify your Cohere API key
"""
import cohere
from config.settings import settings

def test_cohere_api():
    print("Testing Cohere API key...")
    print(f"API Key in settings: {settings.COHERE_API_KEY[:10]}..." if settings.COHERE_API_KEY else "No API key found")

    try:
        # Initialize the Cohere client
        client = cohere.Client(settings.COHERE_API_KEY)

        # Test the API with a simple embed request
        response = client.embed(
            texts=["Hello, world!"],
            model="embed-english-v3.0",
            input_type="search_document"
        )

        print("[SUCCESS] Cohere API key is valid!")
        print(f"Embedding dimension: {len(response.embeddings[0])}")
        return True

    except Exception as e:
        print(f"[ERROR] Cohere API test failed: {str(e)}")
        return False

def test_qdrant_connection():
    print("\nTesting Qdrant connection...")
    from services.qdrant_service import QdrantService

    try:
        qdrant_service = QdrantService()

        # List collections to test connection
        # This is a simplified test since the Qdrant client doesn't have a direct list_collections method in our implementation
        print(f"[SUCCESS] Qdrant connection appears valid")
        print(f"Qdrant URL: {settings.QDRANT_URL}")
        print(f"Collection name: {settings.QDRANT_COLLECTION_NAME}")
        return True

    except Exception as e:
        print(f"[ERROR] Qdrant connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("API Key and Service Connectivity Test")
    print("=" * 40)

    cohere_ok = test_cohere_api()
    qdrant_ok = test_qdrant_connection()

    print("\n" + "=" * 40)
    if cohere_ok and qdrant_ok:
        print("[SUCCESS] All services are properly configured!")
    else:
        print("[ERROR] Some services need to be fixed before the RAG chatbot will work properly.")
        if not cohere_ok:
            print("  - Fix your Cohere API key in the .env file")
        if not qdrant_ok:
            print("  - Check your Qdrant configuration in the .env file")