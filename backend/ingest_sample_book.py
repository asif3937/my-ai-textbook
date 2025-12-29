#!/usr/bin/env python
"""
Script to ingest the sample book into the RAG chatbot system
"""
import json
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from services.book_content_service import BookContentService
from models import BookContent, ContentChunk
import os


def ingest_sample_book():
    """
    Ingest the sample book from sample_book.json into the database
    """
    # Create a local SQLite engine for this script
    local_engine = create_engine("sqlite:///rag_chatbot.db")
    Base = declarative_base()
    Base.metadata.create_all(bind=local_engine)

    # Create a local session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=local_engine)
    db = SessionLocal()

    try:
        # Initialize the book content service
        book_service = BookContentService()

        # Load sample book data
        with open('sample_book.json', 'r', encoding='utf-8') as f:
            sample_book = json.load(f)

        # Ingest the book
        result = book_service.ingest_book_content(
            db=db,
            title=sample_book['title'],
            author=sample_book['author'],
            content=sample_book['content'],
            metadata=sample_book.get('metadata')
        )

        if result:
            print(f"Book successfully ingested!")
            print(f"Book ID: {result['book_id']}")
            print(f"Title: {result['title']}")
            print(f"Status: {result['status']}")
            print(f"Message: {result['message']}")
            print(f"Chunks created: {result['chunks_count']}")
            return result
        else:
            print("Failed to ingest book")
            return None

    except Exception as e:
        print(f"Error during book ingestion: {str(e)}")
        return None
    finally:
        db.close()


if __name__ == "__main__":
    # Check if we have the required API key
    cohere_api_key = os.getenv('COHERE_API_KEY', '').strip()
    if not cohere_api_key or cohere_api_key == 'your_cohere_api_key_here':
        print("Warning: No valid COHERE_API_KEY found in environment. Please add a valid API key to your .env file.")
        print("For local testing, you can use sentence transformers instead by setting the appropriate configuration.")
        print("\nTo use local embeddings:")
        print("1. Install sentence-transformers: pip install sentence-transformers")
        print("2. Update your config to use local embeddings instead of Cohere")
        print("3. Or add a valid COHERE_API_KEY to your .env file")
    else:
        print("Using COHERE_API_KEY from environment")

    ingest_sample_book()