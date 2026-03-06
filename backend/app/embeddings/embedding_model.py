from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from typing import List, Union
from app.config import config

logger = logging.getLogger(__name__)

class EmbeddingModel:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.EMBEDDING_MODEL
        self.model = None
        self.dimension = None
    
    async def load_model(self):
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Model loaded. Embedding dimension: {self.dimension}")
    
    async def encode(self, texts: Union[str, List[str]], batch_size: int = 32) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def get_dimension(self) -> int:
        return self.dimension