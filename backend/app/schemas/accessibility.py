"""Accessibility score schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AccessibilityScoreBase(BaseModel):
    segment_id: int
    accessibility_index: float
    connectivity_score: Optional[float] = None
    alternative_routes_count: Optional[int] = None
    nearest_hospital_km: Optional[float] = None
    nearest_police_km: Optional[float] = None
    mobile_coverage: Optional[str] = "good"


class AccessibilityScoreIn(AccessibilityScoreBase):
    pass


class AccessibilityScoreOut(AccessibilityScoreBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
