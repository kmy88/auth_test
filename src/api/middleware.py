from fastapi import HTTPException, Header, Depends
from typing import Optional
from ..services.auth import AuthService

def get_auth_service() -> AuthService:
    from ..models.database import DatabaseManager
    db_manager = DatabaseManager()
    return AuthService(db_manager)

async def verify_api_key(
    x_api_key: Optional[str] = Header(None),
    auth_service: AuthService = Depends(get_auth_service)
) -> str:
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is required. Please provide X-API-Key header."
        )
    
    if not auth_service.validate_api_key(x_api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key"
        )
    
    return x_api_key