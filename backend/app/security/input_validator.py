from pydantic import BaseModel, Field, validator
from typing import Optional
import re
import logging

logger = logging.getLogger(__name__)

class QueryValidator(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    dataset_id: str = Field(..., min_length=1)
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()

class DatasetValidator(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    
    @validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z0-9_\-\s]+$', v):
            raise ValueError('Dataset name can only contain letters, numbers, spaces, hyphens and underscores')
        return v.strip()