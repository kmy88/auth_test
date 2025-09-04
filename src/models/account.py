from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountCreate(BaseModel):
    alias: str
    username: str
    password: str

class AccountUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class AccountResponse(BaseModel):
    alias: str
    username: str
    password: str

class AccountInfo(BaseModel):
    id: int
    alias: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ApiKeyCreate(BaseModel):
    key_name: str

class ApiKeyResponse(BaseModel):
    key_name: str
    api_key: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True