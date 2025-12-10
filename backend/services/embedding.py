from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info(f"Initialized embedding model: {settings.EMBEDDING_MODEL}")

    def encode(self, texts: List[str]) -> List[List[float]]:
        """Encode a list of texts into embeddings"""
        try:
            embeddings = self.model.encode(texts)
            # Convert to list of lists for JSON serialization
            return [embedding.tolist() for embedding in embeddings]
        except Exception as e:
            logger.error(f"Error encoding texts: {e}")
            return []

    def encode_single(self, text: str) -> List[float]:
        """Encode a single text into an embedding"""
        try:
            embedding = self.model.encode([text])[0]
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            return []

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        # This is a workaround since SentenceTransformer doesn't have a direct method
        # We'll encode a dummy text to get the dimension
        dummy_embedding = self.encode_single("dummy")
        return len(dummy_embedding) if dummy_embedding else settings.EMBEDDING_DIMENSION

    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            emb1 = np.array(embedding1)
            emb2 = np.array(embedding2)
            # Calculate cosine similarity
            cosine_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            return float(cosine_sim)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0