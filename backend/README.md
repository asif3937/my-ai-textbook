# AI Textbook RAG Backend

This is the backend service for the AI-Native Textbook, implementing a Retrieval-Augmented Generation (RAG) system for interactive textbook learning.

## Architecture

The backend consists of:
- **FastAPI**: Web framework for the API
- **Qdrant**: Vector database for document storage and similarity search
- **Sentence Transformers**: For generating text embeddings
- **External LLM**: Integration with language models for response generation

## Features

- RAG-based question answering
- Document chunking and vectorization
- Context-aware responses
- Health and readiness checks
- Rate limiting and security measures

## Setup

### Prerequisites

- Python 3.9+
- Docker and Docker Compose (for local development)
- Qdrant instance (local or cloud)
- PostgreSQL database (Neon or local)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run with Docker Compose (for local development):
```bash
docker-compose up
```

### Environment Variables

- `QDRANT_URL`: URL for Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `QDRANT_COLLECTION_NAME`: Name of the collection to use
- `NEON_DATABASE_URL`: PostgreSQL connection string
- `EMBEDDING_MODEL`: Model to use for embeddings (default: all-MiniLM-L6-v2)
- `LLM_MODEL`: Model to use for generation (e.g., gpt-3.5-turbo)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS

## API Endpoints

- `GET /`: Root endpoint
- `POST /api/v1/chat`: Main chat endpoint
- `GET /api/v1/health`: Health check
- `GET /api/v1/ready`: Readiness check
- `GET /api/v1/live`: Liveness check

## Deployment

The backend can be deployed to platforms like Railway, Render, or any container hosting service.

### Railway Deployment

1. Create a new Railway project
2. Connect your GitHub repository
3. Add the required environment variables
4. Deploy!

### Render Deployment

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables
4. Configure build and start commands