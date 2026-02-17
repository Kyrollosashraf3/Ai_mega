"""
Settings module for Mega AI Agent.
Configuration management using pydantic-settings.
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Settings
    APP_NAME: str = "Mega_AI_Agent"
    APP_VERSION: str = "0.0.1"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    FILE_ALLOWED_TYPES: Optional[List[str]] =  ["text/plain" , "application/pdf"]
    FILE_ALLOWED_SIZE: Optional[int] = 10 # in MB

    FILE_PATH: Path = Path("app/my_files")
    FILE_DEFAULT_CHUNK_SIZE: int =256000 #bytes 
    class config:
        env_file =".env"
        case_sensitive = True 
        
# Create singleton instance
settings = Settings()
