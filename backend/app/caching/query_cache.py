from typing import Dict, Any, Optional
import logging
import hashlib
import json
import time

logger = logging.getLogger(__name__)

class QueryCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def _generate_key(self, query: str, dataset_id: str) -> str:
        key_string = f"{dataset_id}:{query}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    async def get(self, query: str, dataset_id: str) -> Optional[Dict[str, Any]]:
        key = self._generate_key(query, dataset_id)
        
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                logger.info(f"Cache hit for query: {query[:50]}...")
                return entry['data']
            else:
                del self.cache[key]
        
        return None
    
    async def set(self, query: str, dataset_id: str, data: Dict[str, Any]):
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        key = self._generate_key(query, dataset_id)
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
        logger.info(f"Cached query result: {query[:50]}...")
    
    async def clear(self, dataset_id: str = None):
        if dataset_id:
            keys_to_delete = [k for k in self.cache.keys() if k.startswith(dataset_id)]
            for key in keys_to_delete:
                del self.cache[key]
        else:
            self.cache.clear()
        logger.info("Cache cleared")

query_cache = QueryCache()