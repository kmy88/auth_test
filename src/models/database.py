from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    alias = Column(String(50), unique=True, nullable=False)
    encrypted_username = Column(Text, nullable=False)
    encrypted_password = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ApiKey(Base):
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key_name = Column(String(50), unique=True, nullable=False)
    api_key = Column(String(64), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)

class DatabaseManager:
    def __init__(self, db_path: str = "auth_tool.db"):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.init_db()
    
    def init_db(self):
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()
    
    def close_session(self, session):
        session.close()