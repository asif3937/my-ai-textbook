#!/usr/bin/env python
"""
Script to ingest your actual textbook content into the RAG system
using Neon database and Qdrant vector database
"""
import os
import json
import requests
import sys
from pathlib import Path


def read_textbook_content():
    """
    Read the actual textbook content from the textbook directory
    """
    textbook_dir = Path("../textbook/docs")  # Relative to backend directory
    
    if not textbook_dir.exists():
        print(f"[ERROR] Textbook directory not found at {textbook_dir}")
        print("Please verify the textbook directory exists")
        return None
    
    content_parts = []
    
    # Read the main intro file
    intro_file = textbook_dir / "intro.md"
    if intro_file.exists():
        with open(intro_file, 'r', encoding='utf-8') as f:
            content_parts.append(f.read())
    
    # Read content from all subdirectories
    for subdir in textbook_dir.iterdir():
        if subdir.is_dir():
            for md_file in subdir.rglob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Add a header with the file path to maintain context
                        content_with_header = f"\n\n# From: {md_file.relative_to(textbook_dir)}\n\n{content}"
                        content_parts.append(content_with_header)
                except Exception as e:
                    print(f"[WARNING] Could not read file {md_file}: {e}")
    
    if not content_parts:
        print("[ERROR] No content found in textbook directory")
        return None
    
    full_content = "\n\n".join(content_parts)
    print(f"[SUCCESS] Found textbook content with {len(full_content)} characters")
    return full_content


def ingest_textbook_to_rag(content, title="AI Textbook", author="Textbook Authors"):
    """
    Ingest the textbook content to the RAG system via API
    """
    # Prepare the payload for the API
    payload = {
        "title": title,
        "author": author,
        "content": content,
        "metadata": {
            "source": "AI Textbook Project",
            "year": 2023,
            "subject": "Artificial Intelligence",
            "type": "textbook"
        }
    }
    
    # Send the request to your API
    api_url = "http://localhost:12345/api/v1/books/ingest"
    
    try:
        print("[INFO] Sending textbook content to RAG API...")
        response = requests.post(
            api_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] Textbook successfully ingested!")
            print(f"[INFO] Book ID: {result['book_id']}")
            print(f"[INFO] Title: {result['title']}")
            print(f"[INFO] Status: {result['status']}")
            print(f"[INFO] Message: {result['message']}")
            print(f"[INFO] Chunks created: {result.get('chunks_count', 'Unknown')}")
            return result
        else:
            print(f"[ERROR] Failed to ingest textbook: {response.status_code}")
            print(f"[INFO] Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to the API server. Make sure your FastAPI server is running on http://localhost:8000")
        return None
    except Exception as e:
        print(f"[ERROR] Error during textbook ingestion: {str(e)}")
        return None


def main():
    print("[INFO] Starting textbook ingestion to RAG system...")
    print("[INFO] Using Neon database and Qdrant vector database")
    
    # Read the actual textbook content
    content = read_textbook_content()
    
    if not content:
        print("[ERROR] Could not read textbook content. Please check the textbook directory.")
        sys.exit(1)
    
    # Shorten content for display
    display_content = content[:200] + "..." if len(content) > 200 else content
    print(f"[INFO] Content preview: {display_content}")
    
    # Proceed automatically since we're in an automated environment
    print("[INFO] Proceeding with textbook ingestion...")
    
    # Ingest the textbook content
    result = ingest_textbook_to_rag(
        content=content,
        title="AI Textbook",
        author="AI Textbook Authors"
    )
    
    if result:
        print(f"\n[SUCCESS] Your textbook is now ready for RAG-based question answering!")
        print(f"   You can reference it using Book ID: {result['book_id']}")
        print(f"   The content is stored in both Neon database and Qdrant vector database")
    else:
        print("\n[ERROR] Textbook ingestion failed. Please check the errors above.")


if __name__ == "__main__":
    main()