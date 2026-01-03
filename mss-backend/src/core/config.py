"""
Core Configuration Module

Loads and validates environment variables and provides centralized
configuration for the entire application. Uses Pydantic for validation.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ========================================================================
    # Application Settings
    # ========================================================================
    
    APP_NAME: str = Field(default="MSS Financial Analysis API", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    # ========================================================================
    # Server Settings
    # ========================================================================
    
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=4, description="Number of worker processes")

    # ========================================================================
    # Security & CORS
    # ========================================================================
    
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        description="CORS allowed origins"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        description="Allowed hosts"
    )
    CORS_CREDENTIALS: bool = Field(default=True, description="Allow credentials in CORS")
    CORS_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed CORS methods"
    )
    CORS_HEADERS: List[str] = Field(
        default=["*"],
        description="Allowed CORS headers"
    )

    # ========================================================================
    # Authentication
    # ========================================================================
    
    JWT_SECRET: str = Field(default="your-secret-key-change-this-in-production", description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRATION_HOURS: int = Field(default=24, description="JWT expiration in hours")

    # ========================================================================
    # External APIs
    # ========================================================================
    
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    OPENAI_MODEL: str = Field(default="gpt-4-turbo", description="OpenAI model")
    OPENAI_MAX_TOKENS: int = Field(default=2000, description="Max tokens for OpenAI")
    OPENAI_TEMPERATURE: float = Field(default=0.7, description="Temperature for OpenAI")

    # ========================================================================
    # File Upload
    # ========================================================================
    
    MAX_FILE_SIZE: int = Field(default=52428800, description="Max file size in bytes (50MB default)")
    ALLOWED_EXTENSIONS: List[str] = Field(default=[".pdf"], description="Allowed file extensions")
    UPLOAD_DIR: str = Field(default="./uploads", description="Upload directory")

    # ========================================================================
    # Database (Future use)
    # ========================================================================
    
    DATABASE_URL: str = Field(default="", description="Database URL")
    DATABASE_POOL_SIZE: int = Field(default=10, description="Database connection pool size")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra environment variables

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        """Parse comma-separated origins from environment variable."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_hosts(cls, v):
        """Parse comma-separated hosts from environment variable."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    @field_validator("ENVIRONMENT", mode="before")
    @classmethod
    def validate_environment(cls, v):
        """Validate environment is one of allowed values."""
        if v not in ["development", "staging", "production", "testing"]:
            raise ValueError("ENVIRONMENT must be 'development', 'staging', 'production', or 'testing'")
        return v

    def __init__(self, **data):
        """Initialize settings and validate production safety."""
        super().__init__(**data)
        
        # Production safety checks
        if self.ENVIRONMENT == "production":
            if self.DEBUG:
                logger.warning("DEBUG=True in production! Disabling...")
                self.DEBUG = False
            
            if "*" in self.ALLOWED_ORIGINS:
                logger.warning("CORS allow_origins=['*'] in production! Consider restricting...")
            
            if self.JWT_SECRET == "your-secret-key-change-this-in-production":
                raise ValueError("JWT_SECRET not configured for production!")


# Create global settings instance
settings = Settings()

# Log configuration on startup
logger.info(f"Configuration loaded: {settings.ENVIRONMENT.upper()}")
logger.info(f"Debug mode: {settings.DEBUG}")
logger.info(f"Max file size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB")
