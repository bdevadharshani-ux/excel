import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PromptBuilder:
    def __init__(self):
        self.system_prompt = """
You are an expert data analyst assistant. Your role is to answer questions based ONLY on the provided context from the dataset.

Rules:
1. Answer ONLY using information from the provided context
2. If the context doesn't contain enough information, say "I cannot answer this question based on the available data"
3. Be precise and cite specific values from the data
4. Do not make assumptions or use external knowledge
5. Format your answer clearly and concisely
"""
    
    async def build_prompt(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        logger.info("Building RAG prompt")
        
        context_text = self._format_context(context_docs)
        
        prompt = f"""
Context from dataset:
{context_text}

User Question: {query}

Please provide a clear and accurate answer based on the context above.
"""
        
        return prompt
    
    def _format_context(self, docs: List[Dict[str, Any]]) -> str:
        formatted = []
        for i, doc in enumerate(docs, 1):
            formatted.append(f"[Result {i}]")
            formatted.append(doc['text'])
            formatted.append("")
        return "\n".join(formatted)
    
    def get_system_prompt(self) -> str:
        return self.system_prompt