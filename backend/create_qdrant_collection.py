#!/usr/bin/env python
"""
Script to create the required Qdrant collection for the RAG chatbot
"""
from services.qdrant_service import QdrantService
from config.settings import settings


def create_required_collections():
    """
    Create the required collections in Qdrant
    """
    qdrant_service = QdrantService()
    
    # Determine the embedding dimension based on settings
    # For Cohere embeddings, the dimension is typically 1024 for embed-english-v3.0
    # but it can vary based on the model and input type
    # Let's use a common dimension for Cohere embeddings
    embedding_dimension = 1024  # This is typical for Cohere's embed-english-v3.0
    
    print(f"Creating collection '{settings.QDRANT_COLLECTION_NAME}' with dimension {embedding_dimension}")
    
    success = qdrant_service.create_collection(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        vector_size=embedding_dimension
    )
    
    if success:
        print(f"Collection '{settings.QDRANT_COLLECTION_NAME}' created successfully!")
    else:
        print(f"Failed to create collection '{settings.QDRANT_COLLECTION_NAME}'")
        
    return success


if __name__ == "__main__":
    create_required_collections()