import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///auth_tool.db")
    
    MASTER_KEY = os.getenv("MASTER_KEY", None)
    
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", 8000))
    
    API_TITLE = "Personal Account Management API"
    API_DESCRIPTION = "Secure API for managing encrypted personal accounts"
    API_VERSION = "1.0.0"
    
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    ENCRYPTION_KEY_FILE = os.getenv("ENCRYPTION_KEY_FILE", "encryption.key")
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_database_path(cls):
        if cls.DATABASE_URL.startswith("sqlite:///"):
            return cls.DATABASE_URL[10:]
        return "auth_tool.db"

class DevelopmentConfig(Config):
    DEBUG = True
    API_HOST = "127.0.0.1"
    API_PORT = 8000

class ProductionConfig(Config):
    DEBUG = False
    API_HOST = "0.0.0.0"
    API_PORT = 8000

def get_config():
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return ProductionConfig()
    return DevelopmentConfig()

config = get_config()