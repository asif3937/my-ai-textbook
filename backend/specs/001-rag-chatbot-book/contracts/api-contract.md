# API Contract: RAG Chatbot for Book Content

## Base URL
`https://api.example.com/v1`

## Authentication
All API requests require an API key sent in the `Authorization` header:
`Authorization: Bearer {your-api-key}`

## API Endpoints

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
      "paragraph": 3
    }
  ],
  "mode": "full_book|selected_text_only",
  "timestamp": "2025-12-16T10:30:00Z"
}
```

### 3. Get Chat History
`GET /chat/history/{session_id}`

#### Description
Retrieves the chat history for a specific session.

#### Path Parameters
- `session_id`: Unique identifier for the session

#### Response
```json
{
  "session_id": "unique-session-id",
  "history": [
    {
      "query": "First user query",
      "answer": "First system response",
      "citations": [...],
      "timestamp": "2025-12-16T10:30:00Z"
    },
    {
      "query": "Second user query",
      "answer": "Second system response",
      "citations": [...],
      "timestamp": "2025-12-16T10:31:00Z"
    }
  ]
}
```

### 4. Create New Session
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
    "message": "Human-readable error message",
    "details": "Optional additional error details"
  }
}
```

### Common Error Codes
- `INVALID_INPUT`: Request data does not meet validation requirements
- `BOOK_NOT_FOUND`: The specified book ID does not exist
- `CONTENT_NOT_FOUND`: The required content is not available for the request
- `RATE_LIMIT_EXCEEDED`: Request rate limit has been exceeded
- `INTERNAL_ERROR`: An unexpected internal error occurred

## Data Types

### Book Metadata
```json
{
  "isbn": "string",
  "publisher": "string",
  "year": "integer",
  "language": "string",
  "genre": "string"
}
```

### Citation
```json
{
  "text": "string",
  "chapter": "string",
  "page": "integer",
  "paragraph": "integer",
  "vector_id": "string"
}
```