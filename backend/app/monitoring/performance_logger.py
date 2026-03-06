from datetime import datetime, timezone
import logging
from typing import Dict, Any, List
import time

logger = logging.getLogger(__name__)

class PerformanceLogger:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
        self.max_logs = 1000
    
    async def log_query_performance(self, query: str, latency_ms: float, num_results: int, dataset_id: str):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": query[:100],
            "latency_ms": latency_ms,
            "num_results": num_results,
            "dataset_id": dataset_id
        }
        
        self.logs.append(log_entry)
        
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
        
        logger.info(f"Query performance logged - Latency: {latency_ms:.2f}ms")
    
    async def get_performance_stats(self) -> Dict[str, Any]:
        if not self.logs:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0,
                "max_latency_ms": 0,
                "min_latency_ms": 0
            }
        
        latencies = [log['latency_ms'] for log in self.logs]
        
        return {
            "total_queries": len(self.logs),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "max_latency_ms": max(latencies),
            "min_latency_ms": min(latencies),
            "recent_queries": self.logs[-10:]
        }
    
    async def get_recent_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.logs[-limit:]

performance_logger = PerformanceLogger()