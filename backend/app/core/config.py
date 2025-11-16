"""
Application configuration using Pydantic settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union
import os
from pathlib import Path


def _find_env_file() -> str:
    """
    Find .env file in current directory or parent directory (root).
    This allows the same .env file to work for both Docker and non-Docker setups.
    """
    # First check current directory (backend/)
    current_env = Path(".env")
    if current_env.exists():
        return str(current_env)
    
    # Check parent directory (root/arkham/)
    parent_env = Path("..") / ".env"
    if parent_env.exists():
        return str(parent_env.resolve())
    
    # Check if we're in backend/app/core and need to go up more levels
    # This handles the case when config.py is imported from different locations
    config_file = Path(__file__)
    root_env = config_file.parent.parent.parent.parent / ".env"
    if root_env.exists():
        return str(root_env)
    
    # Default to current directory (will create if needed)
    return ".env"


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=_find_env_file(),
        case_sensitive=True
    )
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Mistral AI Configuration
    MISTRAL_API_KEY: str = ""
    
    # CORS Configuration
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://localhost:5173"
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [
        ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cpp", ".c", 
        ".h", ".hpp", ".cs", ".go", ".rs", ".rb", ".php", ".swift",
        ".kt", ".scala", ".r", ".sql", ".html", ".css", ".scss", ".json",
        ".yaml", ".yml", ".xml", ".md", ".txt"
    ]
    
    # Upload Directory
    UPLOAD_DIR: str = "uploads"
    TEMP_DIR: str = "temp"


settings = Settings()

