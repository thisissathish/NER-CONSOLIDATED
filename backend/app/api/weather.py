"""Weather data API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db, make_point
from app.models import WeatherReading
from app.schemas.weather import WeatherReadingIn, WeatherReadingOut

router = APIRouter()


@router.get("/latest", response_model=List[WeatherReadingOut])
def get_latest_weather(hours: int = 6, db: Session = Depends(get_db)):
    """Get latest weather readings within specified hours."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    readings = (
        db.query(WeatherReading)
        .filter(WeatherReading.timestamp >= cutoff)
        .order_by(WeatherReading.timestamp.desc())
        .all()
    )
    return readings


@router.post("/ingest", response_model=WeatherReadingOut)
def ingest_weather(reading: WeatherReadingIn, db: Session = Depends(get_db)):
    """Ingest a weather reading."""
    db_reading = WeatherReading(
        latitude=reading.latitude,
        longitude=reading.longitude,
        location=make_point(reading.longitude, reading.latitude),
        timestamp=reading.timestamp or datetime.utcnow(),
        temperature_c=reading.temperature_c,
        precipitation_mm=reading.precipitation_mm,
        wind_speed_kmh=reading.wind_speed_kmh,
        humidity_percent=reading.humidity_percent,
        visibility_km=reading.visibility_km,
        condition=reading.condition,
        source=reading.source,
        is_synthetic=reading.is_synthetic
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading
