"""Road network schemas."""
from pydantic import BaseModel, ConfigDict


class RoadNodeOut(BaseModel):
    """Road node output schema."""
    id: int
    name: str
    latitude: float
    longitude: float
    node_type: str
    is_synthetic: bool

    model_config = ConfigDict(from_attributes=True)


class RoadSegmentOut(BaseModel):
    """Road segment output schema."""
    id: int
    from_node_id: int
    to_node_id: int
    distance_km: float
    road_name: str | None
    road_type: str
    terrain: str
    is_synthetic: bool

    model_config = ConfigDict(from_attributes=True)
