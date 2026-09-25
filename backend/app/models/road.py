"""Road network models."""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base, get_geom_type


class RoadNode(Base):
    """Road network node (intersection or waypoint)."""

    __tablename__ = "road_nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(get_geom_type('POINT', 4326), nullable=True)
    node_type = Column(String(50), default="waypoint")  # waypoint, junction, town
    is_synthetic = Column(Boolean, default=True)

    # Relationships
    segments_from = relationship("RoadSegment", foreign_keys="RoadSegment.from_node_id", back_populates="from_node")
    segments_to = relationship("RoadSegment", foreign_keys="RoadSegment.to_node_id", back_populates="to_node")


class RoadSegment(Base):
    """Road segment between two nodes."""

    __tablename__ = "road_segments"

    id = Column(Integer, primary_key=True, index=True)
    from_node_id = Column(Integer, ForeignKey("road_nodes.id"), nullable=False)
    to_node_id = Column(Integer, ForeignKey("road_nodes.id"), nullable=False)
    distance_km = Column(Float, nullable=False)
    road_name = Column(String(255))
    road_type = Column(String(50), default="highway")  # highway, arterial, collector
    terrain = Column(String(50), default="flat")  # flat, hilly, mountainous
    geometry = Column(get_geom_type('LINESTRING', 4326), nullable=True)
    is_synthetic = Column(Boolean, default=True)
    extra_metadata = Column("metadata", Text, nullable=True)  # JSON string for additional attributes

    # Relationships
    from_node = relationship("RoadNode", foreign_keys=[from_node_id], back_populates="segments_from")
    to_node = relationship("RoadNode", foreign_keys=[to_node_id], back_populates="segments_to")
    risk_scores = relationship("RiskScore", back_populates="segment")
    accessibility_scores = relationship("AccessibilityScore", back_populates="segment")
