import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class Evaluator:
    def __init__(self):
        self.evaluation_results = []
    
    async def evaluate_response(self, query: str, answer: str, retrieved_docs: List[Dict[str, Any]], scores: List[float]) -> Dict[str, Any]:
        logger.info("Evaluating RAG response")
        
        evaluation = {
            "query_length": len(query.split()),
            "answer_length": len(answer.split()),
            "num_sources": len(retrieved_docs),
            "retrieval_quality": self._assess_retrieval_quality(scores),
            "answer_quality": self._assess_answer_quality(answer)
        }
        
        self.evaluation_results.append(evaluation)
        return evaluation
    
    def _assess_retrieval_quality(self, scores: List[float]) -> str:
        if not scores:
            return "poor"
        
        avg_score = sum(scores) / len(scores)
        
        if avg_score > 0.7:
            return "excellent"
        elif avg_score > 0.5:
            return "good"
        elif avg_score > 0.3:
            return "fair"
        else:
            return "poor"
    
    def _assess_answer_quality(self, answer: str) -> str:
        if not answer or len(answer.strip()) < 10:
            return "poor"
        
        if "cannot answer" in answer.lower():
            return "declined"
        
        if len(answer.split()) > 20:
            return "detailed"
        else:
            return "concise"