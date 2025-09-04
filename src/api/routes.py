from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.account import (
    AccountCreate, AccountUpdate, AccountResponse, 
    AccountInfo, ApiKeyCreate, ApiKeyResponse
)
from ..services.account_manager import AccountManager
from ..services.auth import AuthService
from ..services.encryption import EncryptionService
from ..models.database import DatabaseManager
from .middleware import verify_api_key

router = APIRouter()

def get_dependencies():
    db_manager = DatabaseManager()
    encryption_service = EncryptionService()
    account_manager = AccountManager(db_manager, encryption_service)
    auth_service = AuthService(db_manager)
    return account_manager, auth_service

@router.post("/auth/validate")
async def validate_api_key(api_key: str = Depends(verify_api_key)):
    return {"valid": True, "message": "API key is valid"}

@router.get("/accounts/{alias}", response_model=AccountResponse)
async def get_account(alias: str, api_key: str = Depends(verify_api_key)):
    account_manager, _ = get_dependencies()
    account = account_manager.get_account(alias)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.post("/accounts", response_model=AccountInfo)
async def create_account(
    account: AccountCreate,
    api_key: str = Depends(verify_api_key)
):
    account_manager, _ = get_dependencies()
    try:
        return account_manager.create_account(account)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/accounts/{alias}", response_model=AccountInfo)
async def update_account(
    alias: str,
    account: AccountUpdate,
    api_key: str = Depends(verify_api_key)
):
    account_manager, _ = get_dependencies()
    updated_account = account_manager.update_account(alias, account)
    if not updated_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated_account

@router.delete("/accounts/{alias}")
async def delete_account(alias: str, api_key: str = Depends(verify_api_key)):
    account_manager, _ = get_dependencies()
    if not account_manager.delete_account(alias):
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": f"Account '{alias}' deleted successfully"}

@router.get("/accounts", response_model=List[AccountInfo])
async def list_accounts(api_key: str = Depends(verify_api_key)):
    account_manager, _ = get_dependencies()
    return account_manager.list_accounts()

@router.post("/admin/api-keys", response_model=ApiKeyResponse)
async def create_api_key(key_data: ApiKeyCreate):
    _, auth_service = get_dependencies()
    try:
        return auth_service.create_api_key(key_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/admin/api-keys", response_model=List[ApiKeyResponse])
async def list_api_keys():
    _, auth_service = get_dependencies()
    return auth_service.list_api_keys()

@router.post("/admin/api-keys/{key_name}/deactivate")
async def deactivate_api_key(key_name: str):
    _, auth_service = get_dependencies()
    if not auth_service.deactivate_api_key(key_name):
        raise HTTPException(status_code=404, detail="API key not found")
    return {"message": f"API key '{key_name}' deactivated"}

@router.post("/admin/api-keys/{key_name}/activate")
async def activate_api_key(key_name: str):
    _, auth_service = get_dependencies()
    if not auth_service.activate_api_key(key_name):
        raise HTTPException(status_code=404, detail="API key not found")
    return {"message": f"API key '{key_name}' activated"}

@router.delete("/admin/api-keys/{key_name}")
async def delete_api_key(key_name: str):
    _, auth_service = get_dependencies()
    if not auth_service.delete_api_key(key_name):
        raise HTTPException(status_code=404, detail="API key not found")
    return {"message": f"API key '{key_name}' deleted"}