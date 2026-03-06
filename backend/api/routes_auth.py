from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.security.token_handler import TokenHandler
from app.database import get_database
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user_id: str
    email: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    db = await get_database()
    
    user = await db.users.find_one({"email": request.email}, {"_id": 0})
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not TokenHandler.verify_password(request.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = TokenHandler.create_access_token({"sub": user['user_id'], "email": user['email']})
    
    return LoginResponse(
        token=token,
        user_id=user['user_id'],
        email=user['email']
    )

@router.post("/register")
async def register(request: RegisterRequest):
    db = await get_database()
    
    existing_user = await db.users.find_one({"email": request.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    import uuid
    user_id = str(uuid.uuid4())
    
    hashed_password = TokenHandler.hash_password(request.password)
    
    user = {
        "user_id": user_id,
        "email": request.email,
        "name": request.name,
        "password": hashed_password,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.users.insert_one(user)
    
    return {"message": "User registered successfully", "user_id": user_id}