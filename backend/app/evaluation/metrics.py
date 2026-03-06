import logging
from typing import List, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)

class Metrics:
    @staticmethod
    async def compute_retrieval_metrics(retrieved_docs: List[Dict[str, Any]], scores: List[float], query: str) -> Dict[str, Any]:
        logger.info("Computing retrieval metrics")
        
        metrics = {
            "num_retrieved": len(retrieved_docs),
            "avg_score": float(np.mean(scores)) if scores else 0.0,
            "max_score": float(np.max(scores)) if scores else 0.0,
            "min_score": float(np.min(scores)) if scores else 0.0,
            "score_variance": float(np.var(scores)) if scores else 0.0
        }
        
        if len(scores) >= 5:
            metrics["precision_at_5"] = float(np.mean(scores[:5]))
        
        return metrics
    
    @staticmethod
    async def compute_confidence_score(retrieval_scores: List[float], hallucination_score: float) -> float:
        if not retrieval_scores:
            return 0.0
        
        retrieval_confidence = float(np.mean(retrieval_scores[:3])) if len(retrieval_scores) >= 3 else float(np.mean(retrieval_scores))
        
        combined_confidence = (retrieval_confidence * 0.6) + (hallucination_score * 0.4)
        
        return min(max(combined_confidence, 0.0), 1.0)