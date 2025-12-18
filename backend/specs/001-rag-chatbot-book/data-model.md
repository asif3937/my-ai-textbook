# Data Model: Integrated RAG Chatbot for Book Content

## Entities

### BookContent
Represents the text content of a book, including chapters, pages, and paragraphs that have been processed and indexed for RAG.

**Fields**:
- `id` (UUID): Unique identifier for the book content
- `title` (String): Title of the book
- `author` (String): Author of the book
- `content` (Text): Full text content of the book
- `metadata` (JSON): Additional book metadata (ISBN, publisher, etc.)
- `created_at` (DateTime): Timestamp of when the book was indexed
- `updated_at` (DateTime): Timestamp of last update

**Relationships**:
- One-to-Many with `ContentChunk` (via `book_content_id`)

**Validation Rules**:
- Title and author must not be empty
- Content must not be empty

### ContentChunk
Represents a chunk of book content that has been embedded and stored in the vector database.

**Fields**:
- `id` (UUID): Unique identifier for the chunk
- `book_content_id` (UUID): Reference to the parent BookContent
- `chunk_text` (Text): The actual text of the chunk
- `chunk_metadata` (JSON): Metadata including chapter, page, paragraph
- `embedding_id` (String): ID in the vector database for retrieval
- `vector_id` (String): Vector ID in Qdrant
- `created_at` (DateTime): Timestamp of creation

**Relationships**:
- Many-to-One with `BookContent` (via `book_content_id`)

**Validation Rules**:
- chunk_text must not be empty
- embedding_id must be present

### UserQuery
Represents a question or request from the user that needs to be answered using the book content.

**Fields**:
- `id` (UUID): Unique identifier for the query
- `session_id` (UUID): Reference to the chat session
- `query_text` (String): The actual text of the user's query
- `mode` (Enum): Either 'full_book' or 'selected_text_only'
- `selected_text` (Text, optional): Text selected by the user (if in selected-text mode)
- `created_at` (DateTime): Timestamp of when the query was made

**Relationships**:
- Many-to-One with `Session` (via `session_id`)
- One-to-Many with `RetrievedContext` (via `user_query_id`)

**Validation Rules**:
- query_text must not be empty
- mode must be one of the allowed values
- If mode is 'selected_text_only', then selected_text must not be empty

### RetrievedContext
Represents the relevant passages from the book that are retrieved based on the user's query or selected text.

**Fields**:
- `id` (UUID): Unique identifier for the retrieved context
- `user_query_id` (UUID): Reference to the associated user query
- `content_chunk_id` (UUID): Reference to the ContentChunk that was retrieved
- `relevance_score` (Float): Relevance score of the chunk to the query
- `rank` (Integer): Rank of this chunk in the list of retrieved chunks

**Relationships**:
- Many-to-One with `UserQuery` (via `user_query_id`)
- Many-to-One with `ContentChunk` (via `content_chunk_id`)

**Validation Rules**:
- relevance_score must be between 0 and 1

### GeneratedResponse
The answer provided by the system, grounded in the retrieved context and containing proper citations.

**Fields**:
- `id` (UUID): Unique identifier for the response
- `user_query_id` (UUID): Reference to the associated user query
- `response_text` (Text): The actual text of the generated response
- `citations` (JSON): List of citations mapping to book content
- `response_metadata` (JSON): Additional metadata about the response generation
- `created_at` (DateTime): Timestamp of response creation

**Relationships**:
- Many-to-One with `UserQuery` (via `user_query_id`)
- Many-to-Many with `ContentChunk` (via `retrieved_context` relationship)

**Validation Rules**:
- response_text must not be empty
- citations must be properly formatted

### Session
Represents a user session with the chatbot, tracking conversation history.

**Fields**:
- `id` (UUID): Unique identifier for the session
- `user_id` (UUID, optional): Reference to the authenticated user
- `session_metadata` (JSON): Additional metadata about the session
- `created_at` (DateTime): Timestamp of session creation
- `updated_at` (DateTime): Timestamp of last activity

**Relationships**:
- One-to-Many with `UserQuery` (via `session_id`)
- One-to-Many with `ChatHistory` (via `session_id`)

### ChatHistory
Stores the conversation history between the user and the chatbot.

**Fields**:
- `id` (UUID): Unique identifier for the chat history entry
- `session_id` (UUID): Reference to the associated session
- `user_query_id` (UUID): Reference to the associated user query
- `generated_response_id` (UUID): Reference to the associated generated response
- `created_at` (DateTime): Timestamp of when the exchange occurred

**Relationships**:
- Many-to-One with `Session` (via `session_id`)
- Many-to-One with `UserQuery` (via `user_query_id`)
- Many-to-One with `GeneratedResponse` (via `generated_response_id`)

## State Transitions
There are no specific state transitions for the core entities, as they are primarily data models. However, the overall system has these behavioral transitions:

- When a user initiates a query, the system moves from an idle state to processing the query
- Based on whether text is selected, the system transitions between 'full_book' and 'selected_text_only' modes
- After generating a response, the system transitions to a state where it waits for the next user query