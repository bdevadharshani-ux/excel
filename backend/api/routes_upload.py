from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from pathlib import Path
import uuid
import shutil
from datetime import datetime, timezone
import logging
import pandas as pd

from app.config import config
from app.database import get_database
from app.security.auth import get_current_user
from app.ingestion.excel_loader import ExcelLoader
from app.ingestion.data_cleaner import DataCleaner
from app.ingestion.chunk_builder import ChunkBuilder
from app.embeddings.embedding_pipeline import EmbeddingPipeline
from app.vector_store.faiss_store import FAISSStore
from app.vector_store.keyword_index import KeywordIndex
from app.analytics.stats_engine import StatsEngine
from app.utils.suggestion_generator import SuggestionGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["upload"])

class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    num_rows: int
    num_columns: int
    message: str
    suggestions: list = []

@router.post("", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    logger.info(f"Upload request from user {current_user['email']}")
    
    if not file.filename.endswith(('.xlsx', '.xls', '.xlsm')):
        raise HTTPException(status_code=400, detail="Only Excel files are supported")
    
    dataset_id = str(uuid.uuid4())
    file_path = config.UPLOAD_DIR / f"{dataset_id}_{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        loader = ExcelLoader()
        df = await loader.load_excel(file_path)
        
        cleaner = DataCleaner()
        df_clean = await cleaner.clean_data(df)
        
        chunk_builder = ChunkBuilder()
        chunks = await chunk_builder.build_chunks(df_clean)
        
        embedding_pipeline = EmbeddingPipeline()
        await embedding_pipeline.initialize()
        embeddings, texts = await embedding_pipeline.process_chunks(chunks)
        
        faiss_store = FAISSStore(dataset_id)
        await faiss_store.create_index(embeddings, chunks)
        
        keyword_index = KeywordIndex()
        await keyword_index.build_index(chunks)
        
        stats_engine = StatsEngine()
        stats = await stats_engine.compute_dataset_stats(df_clean)
        
        # Generate query suggestions
        dataset_info = {
            "columns": df_clean.columns.tolist(),
            "num_rows": len(df_clean),
            "stats": stats
        }
        suggestions = SuggestionGenerator.generate_suggestions(dataset_info)
        
        db = await get_database()
        dataset_doc = {
            "dataset_id": dataset_id,
            "user_id": current_user['sub'],
            "filename": file.filename,
            "file_path": str(file_path),
            "num_rows": len(df_clean),
            "num_columns": len(df_clean.columns),
            "columns": df_clean.columns.tolist(),
            "stats": stats,
            "suggestions": suggestions,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "ready"
        }
        await db.datasets.insert_one(dataset_doc)
        
        logger.info(f"Dataset {dataset_id} uploaded and indexed successfully")
        
        return UploadResponse(
            dataset_id=dataset_id,
            filename=file.filename,
            num_rows=len(df_clean),
            num_columns=len(df_clean.columns),
            message="Dataset uploaded and indexed successfully",
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/datasets")
async def list_datasets(current_user: dict = Depends(get_current_user)):
    db = await get_database()
    datasets = await db.datasets.find({"user_id": current_user['sub']}, {"_id": 0}).to_list(100)
    return {"datasets": datasets}