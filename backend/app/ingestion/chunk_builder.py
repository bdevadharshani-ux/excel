import pandas as pd
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ChunkBuilder:
    def __init__(self):
        self.chunks = []
    
    async def build_chunks(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        logger.info("Building document chunks from dataset...")
        chunks = []
        
        for idx, row in df.iterrows():
            text_parts = []
            metadata = {}
            
            for col in df.columns:
                value = row[col]
                if pd.notna(value) and str(value).strip():
                    text_parts.append(f"{col}: {value}")
                    metadata[col] = value
            
            chunk_text = " | ".join(text_parts)
            
            chunk = {
                "id": f"row_{idx}",
                "text": chunk_text,
                "metadata": metadata,
                "row_index": int(idx)
            }
            chunks.append(chunk)
        
        logger.info(f"Created {len(chunks)} document chunks")
        self.chunks = chunks
        return chunks
    
    def get_chunk_by_id(self, chunk_id: str) -> Dict[str, Any]:
        for chunk in self.chunks:
            if chunk['id'] == chunk_id:
                return chunk
        return None