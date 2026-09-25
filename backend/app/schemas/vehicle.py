"""Vehicle tracking schemas."""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class VehiclePositionIn(BaseModel):
    """Vehicle position input schema."""
    latitude: float
    longitude: float
    speed_kmh: Optional[float] = None
    heading: Optional[float] = None
    segment_id: Optional[int] = None


class VehiclePositionOut(BaseModel):
    """Vehicle position output schema."""
    id: int
    vehicle_id: int
    latitude: float
    longitude: float
    timestamp: datetime
    speed_kmh: Optional[float]
    heading: Optional[float]
    segment_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class VehicleOut(BaseModel):
    """Vehicle output schema."""
    id: int
    registration_number: str
    vehicle_type: str
    operator: Optional[str]
    is_active: bool
    current_segment_id: Optional[int]
    is_synthetic: bool

    model_config = ConfigDict(from_attributes=True)
