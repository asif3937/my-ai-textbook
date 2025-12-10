from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = datetime.now()

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    context_limit: int = 5  # Number of context chunks to retrieve
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []
    timestamp: datetime = datetime.now()

class Document(BaseModel):
    id: str
    content: str
    metadata: dict = {}
    embedding: Optional[List[float]] = None

class DocumentChunk(BaseModel):
    id: str
    content: str
    document_id: str
    chunk_index: int
    embedding: Optional[List[float]] = None
    metadata: dict = {}

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: dict = {}

class QueryResponse(BaseModel):
    results: List[DocumentChunk]
    query_embedding: List[float]