import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

class Config:
    MONGO_URL = os.environ.get('MONGO_URL')
    DB_NAME = os.environ.get('DB_NAME')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 1440))
    
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    LLM_PROVIDER = "groq"
    LLM_MODEL = "llama-3.3-70b-versatile"
    
    FAISS_INDEX_PATH = ROOT_DIR / "data" / "faiss_index"
    UPLOAD_DIR = ROOT_DIR / "data" / "uploads"
    
    TOP_K_RETRIEVAL = 10
    TOP_K_RERANK = 5
    
config = Config()

config.FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)
config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)