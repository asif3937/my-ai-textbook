import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from config.settings import settings
import uuid

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME

        # Check if we can use local embeddings
        SENTENCE_TRANSFORMERS_AVAILABLE = False
        try:
            # Try to import and initialize the model to check if everything works
            # We'll only import when we actually need to use it to avoid DLL issues
            import torch
            # If torch imports successfully, try to load the model
            from sentence_transformers import SentenceTransformer
            test_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            SENTENCE_TRANSFORMERS_AVAILABLE = True
            self.embedding_model = test_model
            del test_model  # Clean up
        except Exception as e:
            logger.warning(f"Sentence transformers not available or not working properly: {str(e)}. Local embeddings will not work.")
            logger.warning("This is often due to PyTorch compatibility issues on Windows.")

        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.use_local_embeddings = True
            self.embedding_provider = "local"
        else:
            # Try to use external embedding services
            self.use_local_embeddings = False
            self.embedding_provider = self._setup_external_embeddings()

    def _setup_external_embeddings(self):
        """Setup external embedding service (OpenAI or Cohere)"""
        # Check for OpenAI embeddings first
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip():
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("Using OpenAI for embeddings")
                return "openai"
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI embeddings: {str(e)}")

        # Check for Cohere embeddings
        if settings.COHERE_API_KEY and settings.COHERE_API_KEY.strip():
            try:
                import cohere
                self.cohere_client = cohere.Client(settings.COHERE_API_KEY)
                logger.info("Using Cohere for embeddings")
                return "cohere"
            except Exception as e:
                logger.warning(f"Could not initialize Cohere embeddings: {str(e)}")

        logger.warning("No embedding service available (local, OpenAI, or Cohere)")
        return "none"

    def retrieve_relevant_chunks(self, query: str, book_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant text chunks from the vector store for a given query and book
        """
        try:
            if self.use_local_embeddings:
                # Generate embedding for the query using local model
                query_embedding = self.embedding_model.encode(query).tolist()
            elif self.embedding_provider == "openai":
                # Use OpenAI for embeddings
                response = self.openai_client.embeddings.create(
                    input=query,
                    model="text-embedding-ada-002"  # or another suitable embedding model
                )
                query_embedding = response.data[0].embedding
            elif self.embedding_provider == "cohere":
                # Use Cohere for embeddings
                response = self.cohere_client.embed(
                    texts=[query],
                    model="embed-english-v3.0",  # or another suitable embedding model
                    input_type="search_query"
                )
                query_embedding = response.embeddings[0]
            else:
                # No embedding service available
                logger.warning("No embedding service available, returning empty results")
                return []

            # Search the vector store for relevant chunks
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=None,  # Add a filter for specific book_id if needed
                limit=min(top_k, 10),  # Limit to prevent too many results
                with_payload=True
            )

            # Extract the relevant content from search results
            relevant_chunks = []
            for hit in search_result:
                chunk_data = {
                    'text': hit.payload.get('content', ''),
                    'score': hit.score,
                    'metadata': hit.payload.get('metadata', {}),
                    'source': hit.payload.get('source', 'unknown')
                }
                relevant_chunks.append(chunk_data)

            logger.info(f"Retrieved {len(relevant_chunks)} relevant chunks for query: {query[:50]}...")
            return relevant_chunks

        except Exception as e:
            logger.error(f"Error retrieving relevant chunks: {str(e)}")
            return []

    def retrieve_context_for_selected_text(self, selected_text: str) -> List[Dict[str, Any]]:
        """
        Return context for user-selected text
        """
        if not selected_text.strip():
            return []

        # Simply return the selected text as context
        return [{
            'text': selected_text,
            'score': 1.0,
            'metadata': {'source': 'user_selected'},
            'source': 'user_input'
        }]