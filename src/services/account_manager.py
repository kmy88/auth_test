from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.database import Account, DatabaseManager
from ..models.account import AccountCreate, AccountUpdate, AccountResponse, AccountInfo
from .encryption import EncryptionService

class AccountManager:
    def __init__(self, db_manager: DatabaseManager, encryption_service: EncryptionService):
        self.db_manager = db_manager
        self.encryption_service = encryption_service
    
    def create_account(self, account_data: AccountCreate) -> AccountInfo:
        session = self.db_manager.get_session()
        try:
            existing_account = session.query(Account).filter(Account.alias == account_data.alias).first()
            if existing_account:
                raise ValueError(f"Account with alias '{account_data.alias}' already exists")
            
            encrypted_username = self.encryption_service.encrypt(account_data.username)
            encrypted_password = self.encryption_service.encrypt(account_data.password)
            
            db_account = Account(
                alias=account_data.alias,
                encrypted_username=encrypted_username,
                encrypted_password=encrypted_password
            )
            
            session.add(db_account)
            session.commit()
            session.refresh(db_account)
            
            return AccountInfo.from_orm(db_account)
        finally:
            self.db_manager.close_session(session)
    
    def get_account(self, alias: str) -> Optional[AccountResponse]:
        session = self.db_manager.get_session()
        try:
            db_account = session.query(Account).filter(Account.alias == alias).first()
            if not db_account:
                return None
            
            username = self.encryption_service.decrypt(db_account.encrypted_username)
            password = self.encryption_service.decrypt(db_account.encrypted_password)
            
            return AccountResponse(
                alias=db_account.alias,
                username=username,
                password=password
            )
        finally:
            self.db_manager.close_session(session)
    
    def update_account(self, alias: str, account_data: AccountUpdate) -> Optional[AccountInfo]:
        session = self.db_manager.get_session()
        try:
            db_account = session.query(Account).filter(Account.alias == alias).first()
            if not db_account:
                return None
            
            if account_data.username:
                db_account.encrypted_username = self.encryption_service.encrypt(account_data.username)
            
            if account_data.password:
                db_account.encrypted_password = self.encryption_service.encrypt(account_data.password)
            
            session.commit()
            session.refresh(db_account)
            
            return AccountInfo.from_orm(db_account)
        finally:
            self.db_manager.close_session(session)
    
    def delete_account(self, alias: str) -> bool:
        session = self.db_manager.get_session()
        try:
            db_account = session.query(Account).filter(Account.alias == alias).first()
            if not db_account:
                return False
            
            session.delete(db_account)
            session.commit()
            return True
        finally:
            self.db_manager.close_session(session)
    
    def list_accounts(self) -> List[AccountInfo]:
        session = self.db_manager.get_session()
        try:
            db_accounts = session.query(Account).all()
            return [AccountInfo.from_orm(account) for account in db_accounts]
        finally:
            self.db_manager.close_session(session)