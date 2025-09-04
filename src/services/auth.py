import secrets
import string
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from ..models.database import ApiKey, DatabaseManager
from ..models.account import ApiKeyCreate, ApiKeyResponse

class AuthService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def generate_api_key(self) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(64))
    
    def create_api_key(self, key_data: ApiKeyCreate) -> ApiKeyResponse:
        session = self.db_manager.get_session()
        try:
            existing_key = session.query(ApiKey).filter(ApiKey.key_name == key_data.key_name).first()
            if existing_key:
                raise ValueError(f"API key with name '{key_data.key_name}' already exists")
            
            api_key = self.generate_api_key()
            
            db_api_key = ApiKey(
                key_name=key_data.key_name,
                api_key=api_key,
                is_active=True
            )
            
            session.add(db_api_key)
            session.commit()
            session.refresh(db_api_key)
            
            return ApiKeyResponse.from_orm(db_api_key)
        finally:
            self.db_manager.close_session(session)
    
    def validate_api_key(self, api_key: str) -> bool:
        session = self.db_manager.get_session()
        try:
            db_api_key = session.query(ApiKey).filter(
                ApiKey.api_key == api_key,
                ApiKey.is_active == True
            ).first()
            
            if db_api_key:
                db_api_key.last_used = datetime.utcnow()
                session.commit()
                return True
            return False
        finally:
            self.db_manager.close_session(session)
    
    def get_api_key_info(self, api_key: str) -> Optional[ApiKeyResponse]:
        session = self.db_manager.get_session()
        try:
            db_api_key = session.query(ApiKey).filter(ApiKey.api_key == api_key).first()
            if not db_api_key:
                return None
            return ApiKeyResponse.from_orm(db_api_key)
        finally:
            self.db_manager.close_session(session)
    
    def deactivate_api_key(self, key_name: str) -> bool:
        session = self.db_manager.get_session()
        try:
            db_api_key = session.query(ApiKey).filter(ApiKey.key_name == key_name).first()
            if not db_api_key:
                return False
            
            db_api_key.is_active = False
            session.commit()
            return True
        finally:
            self.db_manager.close_session(session)
    
    def activate_api_key(self, key_name: str) -> bool:
        session = self.db_manager.get_session()
        try:
            db_api_key = session.query(ApiKey).filter(ApiKey.key_name == key_name).first()
            if not db_api_key:
                return False
            
            db_api_key.is_active = True
            session.commit()
            return True
        finally:
            self.db_manager.close_session(session)
    
    def delete_api_key(self, key_name: str) -> bool:
        session = self.db_manager.get_session()
        try:
            db_api_key = session.query(ApiKey).filter(ApiKey.key_name == key_name).first()
            if not db_api_key:
                return False
            
            session.delete(db_api_key)
            session.commit()
            return True
        finally:
            self.db_manager.close_session(session)
    
    def list_api_keys(self) -> list[ApiKeyResponse]:
        session = self.db_manager.get_session()
        try:
            db_api_keys = session.query(ApiKey).all()
            return [ApiKeyResponse.from_orm(key) for key in db_api_keys]
        finally:
            self.db_manager.close_session(session)