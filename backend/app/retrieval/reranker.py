from sentence_transformers import CrossEncoder
import logging
from typing import List, Dict, Any, Tuple
from app.config import config

logger = logging.getLogger(__name__)

class Reranker:
    def __init__(self):
        self.model_name = config.RERANKER_MODEL
        self.model = None
    
    async def load_model(self):
        if self.model is None:
            logger.info(f"Loading reranker model: {self.model_name}")
            self.model = CrossEncoder(self.model_name)
            logger.info("Reranker model loaded")
    
    async def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> Tuple[List[Dict[str, Any]], List[float]]:
        if self.model is None:
            await self.load_model()
        
        logger.info(f"Reranking {len(documents)} documents")
        
        pairs = [[query, doc['text']] for doc in documents]
        
        scores = self.model.predict(pairs)
        
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        top_docs = [doc for doc, score in scored_docs[:top_k]]
        top_scores = [float(score) for doc, score in scored_docs[:top_k]]
        
        logger.info(f"Reranking complete. Top score: {max(top_scores):.4f}")
        return top_docs, top_scores