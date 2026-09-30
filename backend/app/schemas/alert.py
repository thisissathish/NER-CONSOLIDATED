"""Alert schemas."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AlertBase(BaseModel):
    alert_type: str
    severity: str
    title: str
    message: str
    segment_id: Optional[int] = None
    radius_km: Optional[float] = None
    delivery_channels: Optional[str] = "in-app"
    source: Optional[str] = "system"
    expires_at: Optional[datetime] = None


class AlertIn(AlertBase):
    pass


class AlertOut(AlertBase):
    id: int
    timestamp: datetime
    status: str

    class Config:
        from_attributes = True
