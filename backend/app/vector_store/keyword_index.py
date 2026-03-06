from rank_bm25 import BM25Okapi
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

class KeywordIndex:
    def __init__(self):
        self.bm25 = None
        self.chunks = []
        self.tokenized_corpus = []
    
    async def build_index(self, chunks: List[Dict[str, Any]]):
        logger.info("Building BM25 keyword index...")
        
        self.chunks = chunks
        texts = [chunk['text'] for chunk in chunks]
        
        self.tokenized_corpus = [text.lower().split() for text in texts]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        
        logger.info(f"BM25 index built with {len(self.chunks)} documents")
    
    async def search(self, query: str, top_k: int = 10) -> Tuple[List[float], List[int]]:
        if self.bm25 is None:
            raise ValueError("BM25 index not built")
        
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        
        top_indices = scores.argsort()[-top_k:][::-1]
        top_scores = scores[top_indices]
        
        return top_scores.tolist(), top_indices.tolist()