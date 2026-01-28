"""
Configuration management for GitAnalyzer Pro
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_VERSION: str = "v1"
    PROJECT_NAME: str = "GitAnalyzer Pro"
    DEBUG: bool = False
    
    # CORS - comma separated string
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # GitHub Configuration
    GITHUB_TOKEN: Optional[str] = None
    GITHUB_API_URL: str = "https://api.github.com"
    
    # AI Configuration
    AI_PROVIDER: str = "anthropic"  # "anthropic", "openai", or "perplexity"
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    PERPLEXITY_API_KEY: Optional[str] = None
    
    # Model Configuration
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    PERPLEXITY_MODEL: str = "llama-3.1-sonar-large-128k-online"
    AI_MAX_TOKENS: int = 8000
    AI_TEMPERATURE: float = 0.7
    
    # Database/Storage
    DATABASE_URL: str = "sqlite:///./gitanalyzer.db"
    ANALYSIS_RESULTS_DIR: str = "./analysis_results"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Export Configuration
    MAX_EXPORT_SIZE_MB: int = 50
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "/tmp/gitanalyzer.log"
    
    def get_cors_origins(self) -> list:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]
    
    class Config:
        extra = "ignore"
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance"""
    return settings
