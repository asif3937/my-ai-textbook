import os
# Unset the environment variable to force reading from .env file
if 'QDRANT_API_KEY' in os.environ:
    del os.environ['QDRANT_API_KEY']

from services.retrieval_service import RetrievalService

print("Testing RetrievalService with local Qdrant...")

try:
    retrieval_service = RetrievalService()
    print("RetrievalService created")
    
    # Test the connection
    retrieval_service._ensure_qdrant_connection()
    print("Qdrant connection successful!")
    
    # Test initializing a collection
    success = retrieval_service.initialize_collection()
    print(f"Collection initialization success: {success}")
    
    print("All tests passed!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()