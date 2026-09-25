"""Analytics and scoring models."""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class RiskScore(Base):
    """ML-predicted risk score for a road segment."""

    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(Integer, ForeignKey("road_segments.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Risk metrics
    risk_probability = Column(Float, nullable=False)  # 0.0 to 1.0
    risk_category = Column(String(20))  # low, medium, high, critical

    # Contributing factors
    weather_factor = Column(Float)
    terrain_factor = Column(Float)
    historical_factor = Column(Float)

    # Model metadata
    model_version = Column(String(50))
    confidence = Column(Float)

    # Relationships
    segment = relationship("RoadSegment", back_populates="risk_scores")


class AccessibilityScore(Base):
    """GIS-based accessibility score for a road segment."""

    __tablename__ = "accessibility_scores"

    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(Integer, ForeignKey("road_segments.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Accessibility metrics
    accessibility_index = Column(Float, nullable=False)  # 0.0 to 100.0
    connectivity_score = Column(Float)
    alternative_routes_count = Column(Integer)

    # Infrastructure
    nearest_hospital_km = Column(Float)
    nearest_police_km = Column(Float)
    mobile_coverage = Column(String(20))  # none, poor, fair, good, excellent

    # Relationships
    segment = relationship("RoadSegment", back_populates="accessibility_scores")


class Alert(Base):
    """Real-time alert for vehicles and operators."""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    alert_type = Column(String(50), nullable=False)  # weather, disruption, traffic, security
    severity = Column(String(20), nullable=False)  # info, warning, critical
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    # Geographic scope
    segment_id = Column(Integer, ForeignKey("road_segments.id"))
    radius_km = Column(Float)

    # Delivery
    status = Column(String(20), default="active")  # active, acknowledged, resolved
    delivery_channels = Column(String(100))  # JSON list: ["push", "sms", "email"]

    # Metadata
    source = Column(String(100))
    expires_at = Column(DateTime)
