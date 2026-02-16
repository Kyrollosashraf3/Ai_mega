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

    class config:
        env_file =".env"
    

# Create singleton instance
settings = Settings()
