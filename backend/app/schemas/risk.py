"""Risk scoring schemas."""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class RiskScoreOut(BaseModel):
    """Risk score output schema."""
    id: int
    segment_id: int
    timestamp: datetime
    risk_probability: float
    risk_category: Optional[str]
    weather_factor: Optional[float]
    terrain_factor: Optional[float]
    historical_factor: Optional[float]
    model_version: Optional[str]
    confidence: Optional[float]

    model_config = ConfigDict(from_attributes=True)
