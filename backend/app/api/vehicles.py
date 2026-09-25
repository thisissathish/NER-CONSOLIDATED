"""Vehicle tracking API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db, make_point
from app.models import Vehicle, VehiclePosition
from app.schemas.vehicle import VehicleOut, VehiclePositionIn, VehiclePositionOut

router = APIRouter()


@router.get("/", response_model=List[VehicleOut])
def list_vehicles(active_only: bool = True, db: Session = Depends(get_db)):
    """List all vehicles."""
    query = db.query(Vehicle)
    if active_only:
        query = query.filter(Vehicle.is_active == True)
    vehicles = query.all()
    return vehicles


@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Get specific vehicle."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.post("/{vehicle_id}/position", response_model=VehiclePositionOut)
def update_position(vehicle_id: int, position: VehiclePositionIn, db: Session = Depends(get_db)):
    """Update vehicle position."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Create position record
    db_position = VehiclePosition(
        vehicle_id=vehicle_id,
        latitude=position.latitude,
        longitude=position.longitude,
        location=make_point(position.longitude, position.latitude),
        timestamp=datetime.utcnow(),
        speed_kmh=position.speed_kmh,
        heading=position.heading,
        segment_id=position.segment_id
    )
    db.add(db_position)

    # Update vehicle's current segment
    if position.segment_id:
        vehicle.current_segment_id = position.segment_id

    db.commit()
    db.refresh(db_position)

    return db_position


@router.get("/{vehicle_id}/positions", response_model=List[VehiclePositionOut])
def get_vehicle_positions(
    vehicle_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get vehicle position history."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    positions = (
        db.query(VehiclePosition)
        .filter(VehiclePosition.vehicle_id == vehicle_id)
        .order_by(VehiclePosition.timestamp.desc())
        .limit(limit)
        .all()
    )
    return positions
