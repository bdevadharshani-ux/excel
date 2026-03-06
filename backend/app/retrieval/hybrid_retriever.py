import numpy as np
import logging
from typing import List, Dict, Any, Tuple
from app.vector_store.faiss_store import FAISSStore
from app.vector_store.keyword_index import KeywordIndex
from app.embeddings.embedding_pipeline import EmbeddingPipeline

logger = logging.getLogger(__name__)

class HybridRetriever:
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id
        self.faiss_store = FAISSStore(dataset_id)
        self.keyword_index = KeywordIndex()
        self.embedding_pipeline = EmbeddingPipeline()
        self.alpha = 0.7
    
    async def initialize(self, chunks: List[Dict[str, Any]] = None):
        await self.embedding_pipeline.initialize()
        
        try:
            await self.faiss_store.load_index()
            logger.info("Loaded existing FAISS index")
        except FileNotFoundError:
            if chunks:
                logger.info("Creating new indices...")
                embeddings, _ = await self.embedding_pipeline.process_chunks(chunks)
                await self.faiss_store.create_index(embeddings, chunks)
                await self.keyword_index.build_index(chunks)
            else:
                raise ValueError("No existing index and no chunks provided")
        
        if not self.keyword_index.bm25:
            await self.keyword_index.build_index(self.faiss_store.chunks)
    
    async def retrieve(self, query: str, top_k: int = 10) -> Tuple[List[Dict[str, Any]], List[float]]:
        logger.info(f"Hybrid retrieval for query: {query}")
        
        query_embedding = await self.embedding_pipeline.encode_query(query)
        
        vector_scores, vector_indices = await self.faiss_store.search(query_embedding, top_k * 2)
        
        keyword_scores, keyword_indices = await self.keyword_index.search(query, top_k * 2)
        
        combined_scores = self._combine_scores(vector_scores, vector_indices, keyword_scores, keyword_indices)
        
        sorted_items = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        scores = []
        for idx, score in sorted_items:
            chunk = self.faiss_store.get_chunk(idx)
            if chunk:
                results.append(chunk)
                scores.append(float(score))
        
        logger.info(f"Retrieved {len(results)} results")
        return results, scores
    
    def _combine_scores(self, vector_scores, vector_indices, keyword_scores, keyword_indices):
        vector_max = max(vector_scores) if vector_scores else 1.0
        keyword_max = max(keyword_scores) if keyword_scores else 1.0
        
        combined = {}
        
        for score, idx in zip(vector_scores, vector_indices):
            if idx >= 0:
                normalized_score = score / vector_max if vector_max > 0 else 0
                combined[idx] = self.alpha * normalized_score
        
        for score, idx in zip(keyword_scores, keyword_indices):
            if idx >= 0:
                normalized_score = score / keyword_max if keyword_max > 0 else 0
                if idx in combined:
                    combined[idx] += (1 - self.alpha) * normalized_score
                else:
                    combined[idx] = (1 - self.alpha) * normalized_score
        
        return combined