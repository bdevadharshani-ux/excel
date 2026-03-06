from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from app.security.auth import get_current_user
from app.monitoring.performance_logger import performance_logger
from app.database import get_database

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

class PerformanceStats(BaseModel):
    total_queries: int
    avg_latency_ms: float
    max_latency_ms: float
    min_latency_ms: float
    recent_queries: List[Dict[str, Any]]

@router.get("/performance", response_model=PerformanceStats)
async def get_performance_stats(current_user: dict = Depends(get_current_user)):
    stats = await performance_logger.get_performance_stats()
    return PerformanceStats(**stats)

@router.get("/system")
async def get_system_metrics(current_user: dict = Depends(get_current_user)):
    db = await get_database()
    
    total_datasets = await db.datasets.count_documents({"user_id": current_user['sub']})
    total_queries = await db.query_history.count_documents({"user_id": current_user['sub']})
    
    recent_queries = await db.query_history.find(
        {"user_id": current_user['sub']}
    ).sort("timestamp", -1).limit(10).to_list(10)
    
    for query in recent_queries:
        query.pop('_id', None)
    
    return {
        "total_datasets": total_datasets,
        "total_queries": total_queries,
        "recent_queries": recent_queries
    }