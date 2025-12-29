import uvicorn
from main import app
import socket
import random

def find_free_port():
    """Find a free port to use"""
    while True:
        port = random.randint(8000, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                continue  # Try another port

if __name__ == "__main__":
    print("Starting the RAG Chatbot API server...")
    print("Note: Running in fallback mode due to missing local models and invalid API keys.")
    print("The system will work but with limited functionality.")
    
    # Find a free port
    free_port = find_free_port()
    print(f"Using free port: {free_port}")
    print(f"Visit http://0.0.0.0:{free_port}/docs for API documentation")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=free_port,
        reload=False,  # Disable reload for production
        log_level="info"
    )