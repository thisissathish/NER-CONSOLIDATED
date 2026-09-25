"""Field report and disruption models."""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from datetime import datetime

from app.database import Base, get_geom_type


class FieldReport(Base):
    """User-submitted field report."""

    __tablename__ = "field_reports"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(get_geom_type('POINT', 4326), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    report_type = Column(String(50), nullable=False)  # accident, roadblock, congestion, weather, other
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    description = Column(Text, nullable=False)

    # Optional associations
    segment_id = Column(Integer, ForeignKey("road_segments.id"))

    # Metadata
    reporter_id = Column(String(100))
    status = Column(String(20), default="active")  # active, resolved, dismissed
    is_verified = Column(Boolean, default=False)


class DisruptionHistory(Base):
    """Historical disruption events for ML training."""

    __tablename__ = "disruption_history"

    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(Integer, ForeignKey("road_segments.id"), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)

    # Disruption details
    disruption_type = Column(String(50), nullable=False)  # landslide, flooding, accident, roadwork
    severity = Column(String(20))  # low, medium, high, critical
    duration_hours = Column(Float)

    # Environmental factors at time of disruption
    was_monsoon = Column(Boolean, default=False)
    precipitation_mm = Column(Float)
    temperature_c = Column(Float)

    # Data provenance
    is_synthetic = Column(Boolean, default=True)
    source = Column(String(100))
