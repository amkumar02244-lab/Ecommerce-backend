from pydantic_settings import BaseSettings
from typing import List
import os

APP_ENV = os.getenv("APP_ENV", "development")

ENV_FILE_MAP = {
    "development": ".env",
    "staging": ".env.staging",
    "production": ".env.production"
}

class Settings(BaseSettings):
    # App info
    APP_NAME: str = "E-Commerce Backend"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "fallback-secret-key"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # Data directory (kept for backwards compatibility or file uploads if any)
    DATA_DIR: str = "data"

    # Database Settings
    DATABASE_URL: str = "sqlite:///./data/ecommerce.db"

    # JWT Settings — NEW
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    def get_allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ENV_FILE_MAP.get(APP_ENV, ".env")
        extra = "ignore"

settings = Settings()