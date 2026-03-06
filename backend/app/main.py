from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import config
from app.database import connect_to_mongo, close_mongo_connection
from app.logger import setup_logger

from api.routes_auth import router as auth_router
from api.routes_upload import router as upload_router
from api.routes_query import router as query_router
from api.routes_monitoring import router as monitoring_router

logger = setup_logger()

app = FastAPI(
    title="Advanced RAG-Enabled Transformer Embedding System",
    description="Intelligent Knowledge Discovery from Excel Datasets",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting RAG System...")
    try:
        await connect_to_mongo()
        logger.info("RAG System started successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        logger.info("Continuing without MongoDB connection")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down RAG System...")
    try:
        await close_mongo_connection()
    except:
        pass
    logger.info("RAG System shut down")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Advanced RAG-Enabled Transformer Embedding System",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api")
async def api_root():
    return {
        "message": "Advanced RAG-Enabled Transformer Embedding System API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "auth": "/api/auth",
            "upload": "/api/upload",
            "query": "/api/query",
            "monitoring": "/api/monitoring"
        }
    }

@app.get("/api/health")
async def api_health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(monitoring_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
