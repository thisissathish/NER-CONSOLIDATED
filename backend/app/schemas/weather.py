"""Weather data schemas."""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class WeatherReadingIn(BaseModel):
    """Weather reading input schema."""
    latitude: float
    longitude: float
    timestamp: Optional[datetime] = None
    temperature_c: Optional[float] = None
    precipitation_mm: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    humidity_percent: Optional[float] = None
    visibility_km: Optional[float] = None
    condition: Optional[str] = None
    source: str = "openweathermap"
    is_synthetic: bool = False


class WeatherReadingOut(BaseModel):
    """Weather reading output schema."""
    id: int
    latitude: float
    longitude: float
    timestamp: datetime
    temperature_c: Optional[float]
    precipitation_mm: Optional[float]
    wind_speed_kmh: Optional[float]
    humidity_percent: Optional[float]
    visibility_km: Optional[float]
    condition: Optional[str]
    source: str
    is_synthetic: bool

    model_config = ConfigDict(from_attributes=True)
