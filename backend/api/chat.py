from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

from models.chat import ChatRequest, ChatResponse
from services.rag import RAGService

logger = logging.getLogger(__name__)
router = APIRouter()
rag_service = RAGService()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that processes user queries using RAG
    """
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")

        # Process the chat request using RAG service
        response = rag_service.chat(request)

        logger.info(f"Generated response: {response.response[:50]}...")
        return response

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/query")
async def query_endpoint(request: ChatRequest):
    """
    Query endpoint that returns relevant context without generating a full response
    """
    try:
        context_chunks = rag_service.get_relevant_context(
            query=request.message,
            top_k=request.context_limit
        )

        return {
            "query": request.message,
            "results": [chunk.dict() for chunk in context_chunks],
            "count": len(context_chunks)
        }
    except Exception as e:
        logger.error(f"Error in query endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def chat_health():
    """
    Health check for the chat service
    """
    try:
        # Test the RAG service
        test_context = rag_service.get_relevant_context("test", top_k=1)
        return {
            "status": "healthy",
            "vector_db": "connected",
            "message": "Chat service is running"
        }
    except Exception as e:
        logger.error(f"Chat health check failed: {e}")
        raise HTTPException(status_code=503, detail="Chat service is not healthy")