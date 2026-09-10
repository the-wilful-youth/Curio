try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseSettings
    SettingsConfigDict = None

from typing import Optional
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_PROMPTS_DIR = str(PROJECT_ROOT / "prompts")

class Settings(BaseSettings):
    # Database (default to postgresql, supports sqlite for local dev: sqlite:///./content_vault.db)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./content_vault.db")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # AI Provider & Open Models Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "auto")  # auto, groq, openrouter, together, ollama, openai, anthropic
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    TOGETHER_API_KEY: Optional[str] = os.getenv("TOGETHER_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    # Custom endpoint & model for Open Models (e.g. Ollama http://localhost:11434/v1 or custom vLLM)
    AI_BASE_URL: Optional[str] = os.getenv("AI_BASE_URL")
    AI_MODEL: Optional[str] = os.getenv("AI_MODEL")

    # Google Calendar
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/calendar/callback"

    # Storage
    STORAGE_TYPE: str = "local"  # local, s3, r2
    LOCAL_STORAGE_PATH: str = "./storage"

    # Prompts Directory
    PROMPTS_DIR: str = os.getenv("PROMPTS_DIR", DEFAULT_PROMPTS_DIR)

    # App
    APP_SECRET: str = "your-secret-key-change-in-production"
    DEBUG: bool = True

    if SettingsConfigDict:
        model_config = SettingsConfigDict(
            env_file=".env",
            case_sensitive=True,
            extra="ignore"
        )
    else:
        class Config:
            env_file = ".env"
            case_sensitive = True
            extra = "ignore"

settings = Settings()