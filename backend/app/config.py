"""Application configuration."""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "UrbanFlow AI"
    app_version: str = "2.0.0"
    debug: bool = True

    # Database: SQLite by default (zero-docker), or PostgreSQL if configured
    database_url: str = "sqlite:///./urbanflow.db"

    # Redis (Optional)
    redis_url: str = "redis://localhost:6379/0"

    # OpenWeatherMap (Optional)
    openweathermap_api_key: str = ""

    # Default City Bounding Box (Example: Generic Urban Area)
    default_city_name: str = "DemoCity"
    city_min_lat: float = 0.0
    city_max_lat: float = 1.0
    city_min_lon: float = 0.0
    city_max_lon: float = 1.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
