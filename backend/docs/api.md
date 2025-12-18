# RAG Chatbot API Documentation

## Overview
This API provides a Retrieval-Augmented Generation (RAG) chatbot that answers questions based strictly on book content. The system ensures all answers are grounded in the provided text and prevents hallucinations.

## Base URL
`https://your-deployment-url.com/api/v1`

## Authentication
All API requests require an API key sent in the `Authorization` header:
`Authorization: Bearer {your-api-key}`

## Endpoints

### 1. Ingest Book Content
`POST /books/ingest`

#### Description
Ingests book content into the system for RAG processing.

#### Request
```json
{
  "title": "Book Title",
  "author": "Author Name",
  "content": "Full book content as text...",
  "metadata": {
    "isbn": "978-0123456789",
    "publisher": "Publisher Name",
    "year": 2025
  }
}
```

#### Response
```json
{
  "book_id": "unique-book-id",
  "title": "Book Title",
  "status": "processing|completed",
  "message": "Book content ingested successfully"
}
```

### 2. Chat with Book Content
`POST /chat`

#### Description
Queries the RAG system with a question about the book content.

#### Request
```json
{
  "session_id": "unique-session-id",
  "query": "Question about the book content",
  "mode": "full_book|selected_text_only",
  "selected_text": "Optional selected text when in selected_text_only mode",
  "book_id": "unique-book-id"
}
```

#### Response
```json
{
  "session_id": "unique-session-id",
  "response_id": "unique-response-id",
  "answer": "Generated answer based on book content",
  "citations": [
    {
      "text": "Cited passage from the book",
      "chapter": "Chapter Title",
      "page": 42,
      "paragraph": 3,
      "relevance_score": 0.85,
      "validated": true
    }
  ],
  "mode": "full_book|selected_text_only",
  "timestamp": "2025-12-16T10:30:00Z"
}
```

### 3. Create New Session
`POST /sessions`

#### Description
Creates a new chat session.

#### Request
```json
{
  "user_id": "optional-user-id",
  "book_id": "unique-book-id",
  "session_metadata": {
    "device": "web",
    "language": "en"
  }
}
```

#### Response
```json
{
  "session_id": "unique-session-id",
  "created_at": "2025-12-16T10:30:00Z",
  "status": "active"
}
```

## Error Responses

All error responses follow this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

### Common Error Codes
- `INVALID_INPUT`: Request data does not meet validation requirements
- `BOOK_NOT_FOUND`: The specified book ID does not exist
- `CONTENT_NOT_FOUND`: The required content is not available for the request
- `RATE_LIMIT_EXCEEDED`: Request rate limit has been exceeded
- `INTERNAL_ERROR`: An unexpected internal error occurred

## Usage Examples

### Ingesting a Book
```bash
curl -X POST https://your-api-url.com/api/v1/books/ingest \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Book Title",
    "author": "Author Name",
    "content": "Full book content as text..."
  }'
```

### Asking a Question in Full-Book Mode
```bash
curl -X POST https://your-api-url.com/api/v1/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "unique-session-id",
    "query": "What is the main theme of this book?",
    "mode": "full_book",
    "book_id": "unique-book-id"
  }'
```

### Asking a Question in Selected-Text-Only Mode
```bash
curl -X POST https://your-api-url.com/api/v1/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "unique-session-id",
    "query": "Explain this concept in more detail",
    "mode": "selected_text_only",
    "selected_text": "The concept of RAG involves retrieval augmented generation...",
    "book_id": "unique-book-id"
  }'
```