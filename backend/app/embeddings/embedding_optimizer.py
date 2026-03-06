import numpy as np
import logging
from typing import List

logger = logging.getLogger(__name__)

class EmbeddingOptimizer:
    def __init__(self):
        self.stats = {}
    
    async def optimize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        logger.info("Optimizing embeddings...")
        
        embeddings_normalized = self._normalize_embeddings(embeddings)
        
        self.stats = {
            "original_shape": embeddings.shape,
            "optimized_shape": embeddings_normalized.shape,
            "mean_norm": float(np.mean(np.linalg.norm(embeddings_normalized, axis=1)))
        }
        
        return embeddings_normalized
    
    def _normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        return embeddings / norms
    
    def get_stats(self) -> dict:
        return self.stats