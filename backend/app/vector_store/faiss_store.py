import faiss
import numpy as np
import pickle
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any
from app.config import config

logger = logging.getLogger(__name__)

class FAISSStore:
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id
        self.index = None
        self.chunks = []
        self.dimension = None
        self.index_path = config.FAISS_INDEX_PATH / f"{dataset_id}"
        self.index_path.mkdir(parents=True, exist_ok=True)
    
    async def create_index(self, embeddings: np.ndarray, chunks: List[Dict[str, Any]]):
        logger.info(f"Creating FAISS index for dataset {self.dataset_id}")
        
        self.dimension = embeddings.shape[1]
        self.chunks = chunks
        
        embeddings = embeddings.astype('float32')
        
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(embeddings)
        
        logger.info(f"FAISS index created with {self.index.ntotal} vectors")
        
        await self.save_index()
    
    async def search(self, query_embedding: np.ndarray, top_k: int = 10) -> Tuple[List[float], List[int]]:
        if self.index is None:
            raise ValueError("Index not loaded")
        
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        
        distances, indices = self.index.search(query_embedding, top_k)
        
        return distances[0].tolist(), indices[0].tolist()
    
    async def save_index(self):
        index_file = self.index_path / "faiss.index"
        metadata_file = self.index_path / "metadata.pkl"
        
        faiss.write_index(self.index, str(index_file))
        
        with open(metadata_file, 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'dimension': self.dimension
            }, f)
        
        logger.info(f"Index saved to {self.index_path}")
    
    async def load_index(self):
        index_file = self.index_path / "faiss.index"
        metadata_file = self.index_path / "metadata.pkl"
        
        if not index_file.exists():
            raise FileNotFoundError(f"Index not found at {index_file}")
        
        self.index = faiss.read_index(str(index_file))
        
        with open(metadata_file, 'rb') as f:
            metadata = pickle.load(f)
            self.chunks = metadata['chunks']
            self.dimension = metadata['dimension']
        
        logger.info(f"Index loaded from {self.index_path}")
    
    def get_chunk(self, idx: int) -> Dict[str, Any]:
        if 0 <= idx < len(self.chunks):
            return self.chunks[idx]
        return None