import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting the RAG Chatbot API server...")
    print("Note: Running in fallback mode due to missing local models and invalid API keys.")
    print("The system will work but with limited functionality.")
    print("Visit http://0.0.0.0:12345/docs for API documentation")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=12345,  # Changed to port 12345 to avoid conflicts
        reload=False,  # Disable reload for production
        log_level="info"
    )