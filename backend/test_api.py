import requests
import json

# Get the port from the environment or use a default
import os
port = os.environ.get("API_PORT", "12645")  # Use the current port

# Test the health endpoint first
try:
    response = requests.get(f"http://localhost:{port}/api/v1/health")
    print("Health check response:", response.status_code, response.json())
except Exception as e:
    print("Health check failed:", e)

# Test the root endpoint
try:
    response = requests.get(f"http://localhost:{port}/")
    print("Root endpoint response:", response.status_code, response.json())
except Exception as e:
    print("Root endpoint failed:", e)

# Test the chat endpoint with a simple query
try:
    chat_data = {
        "session_id": "test-session-123",
        "query": "What is the capital of France?",
        "book_id": "test-book-123",
        "mode": "full_book"
    }

    response = requests.post(f"http://localhost:{port}/api/v1/chat", json=chat_data)
    print("Chat endpoint response:", response.status_code)
    print("Response body:", response.text)
except Exception as e:
    print("Chat endpoint failed:", e)