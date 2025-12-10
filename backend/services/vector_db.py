from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class VectorDBService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=True
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self._init_collection()

    def _init_collection(self):
        """Initialize the Qdrant collection if it doesn't exist"""
        try:
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=settings.EMBEDDING_DIMENSION,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing collection: {e}")
            raise

    def add_documents(self, documents: List[dict]) -> bool:
        """Add documents to the vector database"""
        try:
            points = []
            for doc in documents:
                points.append(models.PointStruct(
                    id=doc["id"],
                    vector=doc["embedding"],
                    payload={
                        "content": doc["content"],
                        "document_id": doc.get("document_id", ""),
                        "metadata": doc.get("metadata", {}),
                        "chunk_index": doc.get("chunk_index", 0)
                    }
                ))

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Added {len(points)} documents to collection")
            return True
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False

    def search(self, query_vector: List[float], top_k: int = 5, filters: Optional[dict] = None) -> List[dict]:
        """Search for similar documents"""
        try:
            # Convert filters to Qdrant filter format
            qdrant_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        models.FieldCondition(
                            key=f"metadata.{key}",
                            match=models.MatchValue(value=value)
                        )
                    )
                if conditions:
                    qdrant_filter = models.Filter(must=conditions)

            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=qdrant_filter
            )

            return [
                {
                    "id": result.id,
                    "content": result.payload.get("content", ""),
                    "document_id": result.payload.get("document_id", ""),
                    "metadata": result.payload.get("metadata", {}),
                    "chunk_index": result.payload.get("chunk_index", 0),
                    "score": result.score
                }
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

    def delete_document(self, document_id: str) -> bool:
        """Delete a document by its ID"""
        try:
            # Find all points with this document_id
            results = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_id",
                            match=models.MatchValue(value=document_id)
                        )
                    ]
                ),
                limit=10000  # Assuming a document won't have more than 10k chunks
            )

            if results[0]:
                ids_to_delete = [point.id for point in results[0]]
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(
                        points=ids_to_delete
                    )
                )
                logger.info(f"Deleted {len(ids_to_delete)} chunks for document {document_id}")
                return True

            return False
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False

    def get_collection_info(self) -> dict:
        """Get information about the collection"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": info.config.params.vectors.size,
                "vector_size": info.config.params.vectors.size,
                "points_count": info.points_count,
                "indexed_vectors_count": info.indexed_vectors_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}