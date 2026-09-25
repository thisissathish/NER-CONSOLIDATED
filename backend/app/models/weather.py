"""Weather data models."""
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from datetime import datetime

from app.database import Base, get_geom_type


class WeatherReading(Base):
    """Weather observation at a location."""

    __tablename__ = "weather_readings"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(get_geom_type('POINT', 4326), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Weather parameters
    temperature_c = Column(Float)
    precipitation_mm = Column(Float)
    wind_speed_kmh = Column(Float)
    humidity_percent = Column(Float)
    visibility_km = Column(Float)
    condition = Column(String(100))  # clear, rain, fog, snow, etc.

    # Data source
    source = Column(String(50), default="openweathermap")
    is_synthetic = Column(Boolean, default=False)
