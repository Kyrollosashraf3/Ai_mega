"""
Settings module for Mega AI Agent.
Configuration management using pydantic-settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Settings
    APP_NAME: str = "Mega_AI_Agent"
    APP_VERSION: str = "0.0.1"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000


    
    FILE_ALLOWED_TYPES: list = ["text/csv", "application/pdf", "text/plain", "application/json"]
    FILE_ALLOWED_SIZE: int = 10  # in MB


    class config:
        env_file =".env"
    

# Create singleton instance
settings = Settings()
