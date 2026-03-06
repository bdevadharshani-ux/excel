import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class HallucinationDetector:
    def __init__(self):
        self.threshold = 0.3
    
    async def detect(self, answer: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        logger.info("Running hallucination detection")
        
        if not answer or answer.strip() == "":
            return {
                "is_hallucinated": True,
                "confidence": 0.0,
                "reason": "Empty answer"
            }
        
        if "cannot answer" in answer.lower() or "not enough information" in answer.lower():
            return {
                "is_hallucinated": False,
                "confidence": 1.0,
                "reason": "Model appropriately declined to answer"
            }
        
        context_text = " ".join([doc['text'].lower() for doc in context_docs])
        answer_lower = answer.lower()
        
        answer_words = set(answer_lower.split())
        context_words = set(context_text.split())
        
        common_words = answer_words.intersection(context_words)
        overlap_ratio = len(common_words) / len(answer_words) if answer_words else 0
        
        is_hallucinated = overlap_ratio < self.threshold
        
        result = {
            "is_hallucinated": is_hallucinated,
            "confidence": float(overlap_ratio),
            "overlap_ratio": float(overlap_ratio),
            "reason": "Low overlap with context" if is_hallucinated else "Good grounding in context"
        }
        
        logger.info(f"Hallucination detection complete. Overlap: {overlap_ratio:.2f}")
        return result