#!/usr/bin/env python3
"""
Test the backend chat endpoint directly
"""
import requests
import json
import time

def test_chat_endpoint():
    """Test the chat endpoint directly"""
    backend_url = "http://localhost:8000"
    
    print("Testing the chat endpoint...")
    
    # Test payload similar to what frontend sends
    test_payload = {
        "session_id": "test-session",
        "query": "What is this textbook about?",
        "mode": "full_book",
        "book_id": "textbook-content"
    }
    
    print(f"Sending request to: {backend_url}/api/v1/chat")
    print(f"Payload: {json.dumps(test_payload, indent=2)}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{backend_url}/api/v1/chat", 
            json=test_payload,
            timeout=30  # 30 second timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Response received after {duration:.2f} seconds")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error response: {response.text}")
            
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print("Request timed out after 30 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print("Cannot connect to backend. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

def test_ingest_endpoint():
    """Test if we can ingest basic content"""
    backend_url = "http://localhost:8000"
    
    print("\nTesting content ingestion...")
    
    # Sample textbook content
    sample_content = {
        "title": "AI Textbook Sample",
        "author": "Test Author",
        "content": """
        Chapter 1: Introduction to AI
        Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents".
        
        Chapter 2: Machine Learning Basics
        Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data.
        
        Chapter 3: Deep Learning
        Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning.
        """,
        "metadata": {
            "subject": "Artificial Intelligence",
            "level": "beginner"
        }
    }
    
    try:
        response = requests.post(
            f"{backend_url}/api/v1/books/ingest",
            json=sample_content,
            timeout=30
        )
        
        print(f"Ingest status: {response.status_code}")
        if response.status_code == 200:
            print(f"Ingest response: {response.json()}")
        else:
            print(f"Ingest error: {response.text}")
            
        return response.status_code == 200
    except Exception as e:
        print(f"Ingest exception: {e}")
        return False

def test_health():
    """Test health endpoint"""
    backend_url = "http://localhost:8000"
    
    print("\nTesting health endpoint...")
    
    try:
        response = requests.get(f"{backend_url}/api/v1/health")
        print(f"Health status: {response.status_code}")
        if response.status_code == 200:
            print(f"Health response: {response.json()}")
        else:
            print(f"Health error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check exception: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend API functionality...\n")
    
    if test_health():
        print("\n✓ Health check passed")
    else:
        print("\n✗ Health check failed")
    
    success = test_ingest_endpoint()
    if success:
        print("\n✓ Content ingestion test passed")
    else:
        print("\n⚠ Content ingestion test may have failed - this is OK if content already exists")
    
    print("\n" + "="*50)
    print("Now testing chat endpoint...")
    if test_chat_endpoint():
        print("\n✓ Chat endpoint test passed")
    else:
        print("\n✗ Chat endpoint test failed")