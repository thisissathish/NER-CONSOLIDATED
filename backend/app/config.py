"""Application configuration."""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "NER Smart Logistics Platform"
    app_version: str = "1.0.0"
    debug: bool = True

    # Database: SQLite by default (zero-docker), or PostgreSQL if configured
    database_url: str = "sqlite:///./ner_logistics.db"

    # Redis (Optional)
    redis_url: str = "redis://localhost:6379/0"

    # OpenWeatherMap (Optional)
    openweathermap_api_key: str = ""

    # Corridor bounds (Guwahati-Shillong)
    corridor_min_lat: float = 25.5
    corridor_max_lat: float = 26.2
    corridor_min_lon: float = 91.5
    corridor_max_lon: float = 92.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
