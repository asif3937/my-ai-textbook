# Quickstart: Integrated RAG Chatbot for Book Content

This guide will help you set up and run the RAG Chatbot service for book content.

## Prerequisites

- Python 3.9+
- Docker (optional, for containerization)
- Access to Qdrant Cloud
- API keys for Cohere and OpenAI
- PostgreSQL database (Neon recommended)

## Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create your environment file by copying the example:
   ```bash
   cp .env.example .env
   ```

5. Update the `.env` file with your actual API keys and connection strings:
   - `COHERE_API_KEY`
   - `OPENAI_API_KEY`
   - `QDRANT_API_KEY`
   - `QDRANT_CLUSTER_ENDPOINT`
   - `NEON_DATABASE_URL`

## Running the Service

### Local Development

1. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t rag-chatbot .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env rag-chatbot
   ```

## Initial Book Content Setup

1. Prepare your book content in text format
2. Use the content ingestion endpoint to add the book to the system:
   ```bash
   curl -X POST http://localhost:8000/api/v1/books/ingest \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My Book Title",
       "author": "Author Name",
       "content": "Full book content as text..."
     }'
   ```

## Using the Chat API

### Full-Book RAG Mode

Query the system without specifying selected text:

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "unique-session-id",
    "query": "What is the main theme of this book?",
    "mode": "full_book"
  }'
```

### Selected-Text-Only Mode

Query the system with selected text:

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "unique-session-id",
    "query": "Explain this concept in more detail",
    "mode": "selected_text_only",
    "selected_text": "The concept of RAG involves retrieval augmented generation..."
  }'
```

## API Documentation

- Interactive API documentation available at `http://localhost:8000/docs`
- OpenAPI schema available at `http://localhost:8000/openapi.json`

## Testing

Run the test suite:

```bash
pytest
```

For more detailed test results:

```bash
pytest -v
```

## Configuration

The service can be configured via environment variables in the `.env` file:

- `DEBUG`: Enable/disable debug mode (default: false)
- `LOG_LEVEL`: Set the logging level (default: INFO)
- `QDRANT_CLUSTER_ENDPOINT`: Qdrant Cloud endpoint
- `QDRANT_API_KEY`: Qdrant API key
- `COHERE_API_KEY`: Cohere API key for embeddings
- `OPENAI_API_KEY`: OpenAI API key for generation
- `NEON_DATABASE_URL`: PostgreSQL connection string