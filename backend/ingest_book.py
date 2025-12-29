#!/usr/bin/env python
"""
Script to easily ingest books into the RAG chatbot system
"""
import json
import requests
import os
import sys
from pathlib import Path


def ingest_book_from_file(file_path, title, author, metadata=None):
    """
    Ingest a book from a text file into the RAG chatbot system
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        return None
    
    # Read the book content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # If UTF-8 fails, try with different encoding
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Prepare the payload
    payload = {
        "title": title,
        "author": author,
        "content": content,
        "metadata": metadata or {}
    }
    
    # Get the API base URL from environment or use default
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
    
    # Make the API request
    try:
        print(f"Ingesting book '{title}' by {author}...")
        response = requests.post(
            f"{base_url}/books/ingest",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Book successfully ingested!")
            print(f"   Book ID: {result['book_id']}")
            print(f"   Title: {result['title']}")
            print(f"   Status: {result['status']}")
            print(f"   Message: {result['message']}")
            print(f"   Chunks created: {result['chunks_count']}")
            return result
        else:
            print(f"❌ Failed to ingest book: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API server. Make sure your FastAPI server is running on http://localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error during book ingestion: {str(e)}")
        return None


def main():
    if len(sys.argv) < 4:
        print("Usage: python ingest_book.py <book_file_path> <title> <author> [optional_metadata.json]")
        print("\nExample: python ingest_book.py my_book.txt 'My Book Title' 'Author Name'")
        print("Example with metadata: python ingest_book.py my_book.txt 'My Book Title' 'Author Name' metadata.json")
        return
    
    file_path = sys.argv[1]
    title = sys.argv[2]
    author = sys.argv[3]
    
    # Check if metadata file is provided
    metadata = None
    if len(sys.argv) > 4:
        metadata_file = sys.argv[4]
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            print(f"Warning: Metadata file {metadata_file} not found, proceeding without metadata")
    
    # Ingest the book
    result = ingest_book_from_file(file_path, title, author, metadata)
    
    if result:
        print(f"\n🎉 Your book '{title}' is now ready for RAG-based question answering!")
        print(f"   You can reference it using Book ID: {result['book_id']}")
    else:
        print("\n❌ Book ingestion failed. Please check the errors above.")


if __name__ == "__main__":
    main()