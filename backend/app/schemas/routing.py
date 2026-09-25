"""Routing schemas."""
from pydantic import BaseModel
from typing import List, Optional


class RouteRequest(BaseModel):
    """Route request schema."""
    from_node_id: int
    to_node_id: int
    mode: str = "balanced"  # balanced, safest, fastest


class RouteSegmentInfo(BaseModel):
    """Information about a segment in the route."""
    segment_id: int
    from_node_id: int
    to_node_id: int
    distance_km: float
    risk_probability: Optional[float] = None
    estimated_time_minutes: Optional[float] = None


class RouteResponse(BaseModel):
    """Route response schema."""
    from_node_id: int
    to_node_id: int
    mode: str
    total_distance_km: float
    estimated_time_minutes: float
    average_risk: float
    max_risk: float
    segments: List[RouteSegmentInfo]
    node_sequence: List[int]
