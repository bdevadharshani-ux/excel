import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class QueryRewriter:
    def __init__(self):
        self.rewrite_patterns = {}
    
    async def rewrite_query(self, query: str) -> List[str]:
        logger.info(f"Rewriting query: {query}")
        
        queries = [query]
        
        query_lower = query.lower().strip()
        if query_lower != query:
            queries.append(query_lower)
        
        synonyms = await self._expand_with_synonyms(query)
        queries.extend(synonyms)
        
        queries = list(set(queries))
        
        logger.info(f"Generated {len(queries)} query variations")
        return queries
    
    async def _expand_with_synonyms(self, query: str) -> List[str]:
        expansions = []
        
        synonym_map = {
            'total': ['sum', 'aggregate', 'combined'],
            'average': ['mean', 'avg'],
            'maximum': ['max', 'highest', 'peak'],
            'minimum': ['min', 'lowest']
        }
        
        words = query.lower().split()
        for word in words:
            if word in synonym_map:
                for synonym in synonym_map[word]:
                    new_query = query.lower().replace(word, synonym)
                    if new_query != query.lower():
                        expansions.append(new_query)
        
        return expansions[:2]