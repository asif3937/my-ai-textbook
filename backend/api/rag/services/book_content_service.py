import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from config.settings import settings
import uuid
# Import the BookContent model from the root models directory
# Since we're running from the backend directory, we can import models directly
from models import BookContent as Book  # Using the main BookContent model from root models

logger = logging.getLogger(__name__)

class BookContentService:
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

    def ingest_book_content(self, db: Session, title: str, author: str, content: str, metadata: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Ingest book content into the vector store
        """
        try:
            # Create a new book record in the database
            book_id = str(uuid.uuid4())
            book = Book(
                id=uuid.UUID(book_id),
                title=title,
                author=author,
                content=content,  # Store the full content in the root model
                metadata_json=metadata or {}  # Use the field name from root model
            )
            db.add(book)
            db.commit()
            db.refresh(book)

            # Split the content into chunks
            chunks = self._split_content_into_chunks(content)

            # Prepare points for Qdrant
            points = []
            for idx, chunk in enumerate(chunks):
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{book_id}_{idx}"))

                # Generate embedding for the chunk
                if self.use_local_embeddings:
                    embedding = self.embedding_model.encode(chunk).tolist()
                elif self.embedding_provider == "openai":
                    # Use OpenAI for embeddings
                    response = self.openai_client.embeddings.create(
                        input=chunk,
                        model="text-embedding-ada-002"  # or another suitable embedding model
                    )
                    embedding = response.data[0].embedding
                elif self.embedding_provider == "cohere":
                    # Use Cohere for embeddings
                    response = self.cohere_client.embed(
                        texts=[chunk],
                        model="embed-english-v3.0",  # or another suitable embedding model
                        input_type="search_document"
                    )
                    embedding = response.embeddings[0]
                else:
                    logger.error("Cannot ingest content: no embedding service available")
                    db.rollback()
                    return None

                payload = {
                    "content": chunk,
                    "book_id": book_id,
                    "title": title,
                    "author": author,
                    "chunk_index": idx,
                    "metadata": metadata or {}
                }

                points.append({
                    "id": point_id,
                    "vector": embedding,
                    "payload": payload
                })

            # Upload points to Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Ingested book '{title}' with {len(chunks)} chunks")
            return {
                "book_id": book_id,
                "title": title,
                "status": "success",
                "message": f"Successfully ingested book with {len(chunks)} content chunks"
            }
        except Exception as e:
            logger.error(f"Error ingesting book content: {str(e)}")
            db.rollback()
            return None

    def get_book_content(self, db: Session, book_id: str) -> Optional[Book]:
        """
        Retrieve book content from the database
        """
        try:
            book = db.query(Book).filter(Book.id == uuid.UUID(book_id)).first()
            return book
        except Exception as e:
            logger.error(f"Error retrieving book content: {str(e)}")
            return None

    def _split_content_into_chunks(self, content: str, chunk_size: int = 500, overlap: int = 50) -> list:
        """
        Split content into overlapping chunks of specified size
        """
        words = content.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            
        return chunks