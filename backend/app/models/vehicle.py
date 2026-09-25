"""Vehicle tracking models."""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base, get_geom_type


class Vehicle(Base):
    """Vehicle being tracked."""

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String(50), unique=True, nullable=False, index=True)
    vehicle_type = Column(String(50), default="truck")  # truck, bus, car
    operator = Column(String(255))
    is_active = Column(Boolean, default=True)
    current_segment_id = Column(Integer, ForeignKey("road_segments.id"))
    is_synthetic = Column(Boolean, default=True)

    # Relationships
    positions = relationship("VehiclePosition", back_populates="vehicle", order_by="VehiclePosition.timestamp.desc()")
    current_segment = relationship("RoadSegment")


class VehiclePosition(Base):
    """Historical vehicle position."""

    __tablename__ = "vehicle_positions"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(get_geom_type('POINT', 4326), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    speed_kmh = Column(Float)
    heading = Column(Float)  # 0-360 degrees
    segment_id = Column(Integer, ForeignKey("road_segments.id"))

    # Relationships
    vehicle = relationship("Vehicle", back_populates="positions")
    segment = relationship("RoadSegment")
