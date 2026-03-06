from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import time

from app.database import get_database
from app.security.auth import get_current_user
from app.security.input_validator import QueryValidator
from app.retrieval.query_rewriter import QueryRewriter
from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.reranker import Reranker
from app.generation.prompt_builder import PromptBuilder
from app.generation.llm_generator import LLMGenerator
from app.generation.hallucination_detector import HallucinationDetector
from app.evaluation.metrics import Metrics
from app.evaluation.evaluator import Evaluator
from app.caching.query_cache import query_cache
from app.monitoring.performance_logger import performance_logger
from app.utils.excel_exporter import ExcelExporter
from app.config import config

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["query"])

class QueryRequest(BaseModel):
    query: str
    dataset_id: str
    dataset_ids: Optional[List[str]] = None  # For multi-dataset querying
    use_cache: Optional[bool] = True

class QueryResponse(BaseModel):
    answer: str
    supporting_rows: List[Dict[str, Any]]
    similarity_scores: List[float]
    confidence_score: float
    retrieval_metrics: Dict[str, Any]
    latency_ms: float
    cached: bool = False
    query_id: Optional[str] = None

@router.post("", response_model=QueryResponse)
async def query_dataset(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    start_time = time.time()
    
    logger.info(f"Query request from user {current_user['email']}: {request.query}")
    
    # Support both single and multi-dataset querying
    dataset_ids = request.dataset_ids if request.dataset_ids else [request.dataset_id]
    
    validator = QueryValidator(query=request.query, dataset_id=dataset_ids[0])
    
    db = await get_database()
    
    # Verify all datasets exist and user has access
    datasets = []
    for dataset_id in dataset_ids:
        dataset = await db.datasets.find_one({"dataset_id": dataset_id}, {"_id": 0})
        if not dataset:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        if dataset['user_id'] != current_user['sub']:
            raise HTTPException(status_code=403, detail="Access denied")
        datasets.append(dataset)
    
    # Check cache for single dataset queries
    if len(dataset_ids) == 1 and request.use_cache:
        cached_result = await query_cache.get(request.query, dataset_ids[0])
        if cached_result:
            cached_result['cached'] = True
            return cached_result
    
    try:
        query_rewriter = QueryRewriter()
        query_variations = await query_rewriter.rewrite_query(request.query)
        primary_query = query_variations[0]
        
        # Multi-dataset retrieval
        all_retrieved_docs = []
        all_scores = []
        
        for dataset_id in dataset_ids:
            retriever = HybridRetriever(dataset_id)
            await retriever.initialize()
            
            retrieved_docs, initial_scores = await retriever.retrieve(primary_query, config.TOP_K_RETRIEVAL)
            all_retrieved_docs.extend(retrieved_docs)
            all_scores.extend(initial_scores)
        
        # Sort by scores and take top K
        combined = list(zip(all_retrieved_docs, all_scores))
        combined.sort(key=lambda x: x[1], reverse=True)
        top_docs = [doc for doc, _ in combined[:config.TOP_K_RETRIEVAL]]
        top_scores = [score for _, score in combined[:config.TOP_K_RETRIEVAL]]
        
        # Rerank
        reranker = Reranker()
        await reranker.load_model()
        reranked_docs, reranked_scores = await reranker.rerank(request.query, top_docs, config.TOP_K_RERANK)
        
        # Generate answer
        prompt_builder = PromptBuilder()
        system_prompt = prompt_builder.get_system_prompt()
        user_prompt = await prompt_builder.build_prompt(request.query, reranked_docs)
        
        llm_generator = LLMGenerator()
        generation_result = await llm_generator.generate(system_prompt, user_prompt)
        answer = generation_result['answer']
        
        # Hallucination detection
        hallucination_detector = HallucinationDetector()
        hallucination_result = await hallucination_detector.detect(answer, reranked_docs)
        
        # Metrics
        retrieval_metrics = await Metrics.compute_retrieval_metrics(reranked_docs, reranked_scores, request.query)
        confidence_score = await Metrics.compute_confidence_score(reranked_scores, hallucination_result['confidence'])
        
        # Evaluation
        evaluator = Evaluator()
        evaluation = await evaluator.evaluate_response(request.query, answer, reranked_docs, reranked_scores)
        
        latency_ms = (time.time() - start_time) * 1000
        
        await performance_logger.log_query_performance(
            query=request.query,
            latency_ms=latency_ms,
            num_results=len(reranked_docs),
            dataset_id=",".join(dataset_ids)
        )
        
        supporting_rows = []
        for doc in reranked_docs:
            supporting_rows.append({
                "row_id": doc['id'],
                "data": doc['metadata'],
                "text": doc['text']
            })
        
        # Save to query history
        import uuid
        query_id = str(uuid.uuid4())
        
        query_history = {
            "query_id": query_id,
            "user_id": current_user['sub'],
            "dataset_ids": dataset_ids,
            "query": request.query,
            "answer": answer,
            "supporting_rows": supporting_rows,
            "similarity_scores": reranked_scores,
            "confidence_score": confidence_score,
            "latency_ms": latency_ms,
            "timestamp": time.time()
        }
        await db.query_history.insert_one(query_history)
        
        response = QueryResponse(
            answer=answer,
            supporting_rows=supporting_rows,
            similarity_scores=reranked_scores,
            confidence_score=confidence_score,
            retrieval_metrics=retrieval_metrics,
            latency_ms=latency_ms,
            cached=False,
            query_id=query_id
        )
        
        if len(dataset_ids) == 1 and request.use_cache:
            await query_cache.set(request.query, dataset_ids[0], response.model_dump())
        
        logger.info(f"Query processed successfully in {latency_ms:.2f}ms")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/history")
async def get_query_history(limit: int = 20, current_user: dict = Depends(get_current_user)):
    """Get user's query history"""
    db = await get_database()
    
    history = await db.query_history.find(
        {"user_id": current_user['sub']},
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit).to_list(limit)
    
    return {"history": history}

@router.get("/export/{query_id}")
async def export_query_result(query_id: str, current_user: dict = Depends(get_current_user)):
    """Export query result to Excel"""
    db = await get_database()
    
    query_record = await db.query_history.find_one(
        {"query_id": query_id, "user_id": current_user['sub']},
        {"_id": 0}
    )
    
    if not query_record:
        raise HTTPException(status_code=404, detail="Query not found")
    
    # Generate Excel file
    excel_file = ExcelExporter.export_query_results(
        query=query_record['query'],
        answer=query_record['answer'],
        supporting_rows=query_record['supporting_rows'],
        confidence_score=query_record['confidence_score'],
        latency_ms=query_record['latency_ms']
    )
    
    filename = f"query_result_{query_id[:8]}.xlsx"
    
    return Response(
        content=excel_file.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
