#!/usr/bin/env python3
"""
Test script to verify backend API connectivity
"""
import requests
import sys

def test_backend_health():
    """Test if backend is running and accessible"""
    backend_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{backend_url}/api/v1/health")
        if response.status_code == 200:
            print("[SUCCESS] Backend is running and accessible")
            print(f"Health check response: {response.json()}")
            return True
        else:
            print(f"[ERROR] Backend returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to backend at {backend_url}")
        print("Make sure the backend is running with: uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"[ERROR] Exception connecting to backend: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint specifically"""
    backend_url = "http://localhost:8000"
    
    test_payload = {
        "session_id": "test-session",
        "query": "test",
        "mode": "full_book",
        "book_id": "test-book"
    }
    
    try:
        response = requests.post(f"{backend_url}/api/v1/chat", json=test_payload)
        print(f"Chat endpoint response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"[ERROR] Exception calling chat endpoint: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend API connectivity...\n")
    
    if test_backend_health():
        print("\nTesting chat endpoint...")
        test_chat_endpoint()
    else:
        print("\nBackend is not accessible. Please start it with:")
        print("cd backend")
        print("uvicorn main:app --reload")