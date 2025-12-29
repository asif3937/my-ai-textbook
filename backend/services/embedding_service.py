from typing import List, Tuple
import cohere
from config.settings import settings
from utils import logger
import numpy as np

# Import for local embeddings fallback
LOCAL_EMBEDDING_AVAILABLE = False
try:
    from sentence_transformers import SentenceTransformer
    # Try to initialize a basic model to check if everything works
    test_model = SentenceTransformer('all-MiniLM-L6-v2')
    LOCAL_EMBEDDING_AVAILABLE = True
    del test_model  # Clean up
except Exception as e:
    logger.warning(f"Sentence transformers not available or not working properly: {str(e)}. Local embeddings will not work.")
    logger.warning("This is often due to PyTorch compatibility issues on Windows.")


class EmbeddingService:
    def __init__(self):
        # Check if we should use local embeddings
        if settings.LANGUAGE_MODEL_PROVIDER == 'local' and LOCAL_EMBEDDING_AVAILABLE:
            self.use_local = True
            self.local_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Using local embedding model")
        elif settings.COHERE_API_KEY and settings.COHERE_API_KEY.strip():
            self.use_local = False
            self.client = cohere.Client(settings.COHERE_API_KEY)
            self.model = "embed-english-v3.0"  # Using Cohere's embedding model
            logger.info("Using Cohere embedding model")
        else:
            # Default to local if available, otherwise raise an error
            if LOCAL_EMBEDDING_AVAILABLE:
                self.use_local = True
                self.local_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Using local embedding model as fallback")
            else:
                # If no services are available, set up a basic fallback
                logger.warning("No embedding service available. Using basic fallback (not recommended for production).")
                self.use_local = False
                self.fallback_mode = True
                # Create a basic embedding function that returns dummy embeddings
                # This is just to allow the system to run in fallback mode
                self._create_dummy_embeddings()

    def _create_dummy_embeddings(self):
        """Create dummy embeddings for fallback mode"""
        import numpy as np
        # Create a simple function to generate deterministic dummy embeddings
        # based on the hash of the text
        def dummy_embed(texts):
            embeddings = []
            for text in texts:
                # Create a simple hash-based embedding (1024 dimensions)
                # This is just for the system to run, not for actual semantic similarity
                text_hash = hash(text) % (2**32)
                embedding = [(text_hash >> i) % 256 for i in range(1024)]
                # Normalize the embedding
                norm = sum(x**2 for x in embedding) ** 0.5
                if norm == 0:
                    norm = 1
                embedding = [x/norm for x in embedding]
                embeddings.append(embedding)
            return embeddings
        self.dummy_embed = dummy_embed

    def create_embeddings(self, texts: List[str], input_type: str = "search_document") -> List[List[float]]:
        """
        Create embeddings for a list of texts

        Args:
            texts: List of texts to embed
            input_type: The type of input ("search_query" or "search_document")

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        try:
            # Check if we're in fallback mode
            if hasattr(self, 'fallback_mode') and self.fallback_mode:
                # Use dummy embeddings
                embeddings = self.dummy_embed(texts)
                logger.info(f"Created dummy embeddings for {len(texts)} texts in fallback mode")
                return embeddings

            if self.use_local:
                # Use local sentence transformer model
                embeddings = self.local_model.encode(texts).tolist()
                logger.info(f"Created local embeddings for {len(texts)} texts")
                return embeddings
            else:
                # Use Cohere API
                response = self.client.embed(
                    texts=texts,
                    model=self.model,
                    input_type=input_type
                )

                embeddings = [embedding for embedding in response.embeddings]
                logger.info(f"Created Cohere embeddings for {len(texts)} texts")
                return embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise
    
    def create_embedding(self, text: str, input_type: str = "search_document") -> List[float]:
        """
        Create embedding for a single text
        
        Args:
            text: Text to embed
            input_type: The type of input ("search_query" or "search_document")
        
        Returns:
            Embedding as a list of floats
        """
        embeddings = self.create_embeddings([text], input_type)
        return embeddings[0] if embeddings else []
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
        
        Returns:
            Cosine similarity score between -1 and 1
        """
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        
        # Calculate magnitudes
        magnitude1 = sum(a * a for a in embedding1) ** 0.5
        magnitude2 = sum(b * b for b in embedding2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        cosine_similarity = dot_product / (magnitude1 * magnitude2)
        return cosine_similarity