"""Field report schemas."""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class FieldReportIn(BaseModel):
    """Field report input schema."""
    latitude: float
    longitude: float
    report_type: str  # accident, roadblock, congestion, weather, other
    severity: str = "medium"  # low, medium, high, critical
    description: str
    segment_id: Optional[int] = None
    reporter_id: Optional[str] = None


class FieldReportOut(BaseModel):
    """Field report output schema."""
    id: int
    latitude: float
    longitude: float
    timestamp: datetime
    report_type: str
    severity: str
    description: str
    segment_id: Optional[int]
    reporter_id: Optional[str]
    status: str
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)
