"""Road network API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import RoadNode, RoadSegment
from app.schemas.road import RoadNodeOut, RoadSegmentOut

router = APIRouter()


@router.get("/", response_model=List[RoadSegmentOut])
def list_segments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all road segments."""
    segments = db.query(RoadSegment).offset(skip).limit(limit).all()
    return segments


@router.get("/{segment_id}", response_model=RoadSegmentOut)
def get_segment(segment_id: int, db: Session = Depends(get_db)):
    """Get specific road segment."""
    segment = db.query(RoadSegment).filter(RoadSegment.id == segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    return segment


@router.get("/nodes/", response_model=List[RoadNodeOut])
def list_nodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all road nodes."""
    nodes = db.query(RoadNode).offset(skip).limit(limit).all()
    return nodes
