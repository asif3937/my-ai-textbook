import asyncio
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import get_db
from models import Base, BookContent
from config.settings import settings
from services.retrieval_service import RetrievalService
from services.qdrant_service import QdrantService

async def test_qdrant_connection():
    """Test Qdrant connection separately"""
    try:
        print("Testing Qdrant connection...")
        retrieval_service = RetrievalService()
        retrieval_service._ensure_qdrant_connection()
        print("Qdrant connection successful!")
        return True
    except Exception as e:
        print(f"Qdrant connection failed: {e}")
        return False

async def test_qdrant_service():
    """Test the Qdrant service directly"""
    try:
        print("Testing Qdrant service directly...")
        qdrant_service = QdrantService()
        # This should initialize the client
        qdrant_service._ensure_client()
        # Now test a simple operation
        collections = qdrant_service.client.get_collections()
        print("Qdrant service connection successful!")
        print(f"Found {len(collections.collections)} collections")
        return True
    except Exception as e:
        print(f"Qdrant service connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing retrieval service...")
    asyncio.run(test_qdrant_connection())
    print("\nTesting Qdrant service directly...")
    asyncio.run(test_qdrant_service())