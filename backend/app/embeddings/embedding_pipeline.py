import logging
from typing import List, Dict, Any
import numpy as np
from app.embeddings.embedding_model import EmbeddingModel
from app.embeddings.embedding_optimizer import EmbeddingOptimizer

logger = logging.getLogger(__name__)

class EmbeddingPipeline:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.optimizer = EmbeddingOptimizer()
        self.is_initialized = False
    
    async def initialize(self):
        if not self.is_initialized:
            await self.embedding_model.load_model()
            self.is_initialized = True
            logger.info("Embedding pipeline initialized")
    
    async def process_chunks(self, chunks: List[Dict[str, Any]]) -> tuple:
        if not self.is_initialized:
            await self.initialize()
        
        texts = [chunk['text'] for chunk in chunks]
        
        logger.info(f"Encoding {len(texts)} texts...")
        embeddings = await self.embedding_model.encode(texts)
        
        logger.info("Optimizing embeddings...")
        embeddings_optimized = await self.optimizer.optimize_embeddings(embeddings)
        
        return embeddings_optimized, texts
    
    async def encode_query(self, query: str) -> np.ndarray:
        if not self.is_initialized:
            await self.initialize()
        
        embedding = await self.embedding_model.encode(query)
        optimized = await self.optimizer.optimize_embeddings(embedding)
        return optimized[0]
    
    def get_dimension(self) -> int:
        return self.embedding_model.get_dimension()