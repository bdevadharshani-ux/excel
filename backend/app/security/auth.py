from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.security.token_handler import TokenHandler
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    payload = TokenHandler.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return payload