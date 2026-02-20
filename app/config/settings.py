"""
Settings module for Mega AI Agent.
Configuration management using pydantic-settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Settings
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    HOST: str
    PORT: int

    OPEN_AI_KEY: str

    FILE_ALLOWED_TYPES: List[str]
    FILE_ALLOWED_SIZE: int 

    FILE_PATH: Path
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'
    )

# Create singleton instance
settings = Settings()
