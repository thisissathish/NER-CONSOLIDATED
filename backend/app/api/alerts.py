"""Alert API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Alert
from app.schemas.alert import AlertIn, AlertOut

router = APIRouter()


@router.get("/", response_model=List[AlertOut])
def list_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all alerts with optional filtering."""
    query = db.query(Alert)
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    alerts = query.order_by(Alert.timestamp.desc()).offset(skip).limit(limit).all()
    return alerts


@router.post("/", response_model=AlertOut)
def create_alert(alert: AlertIn, db: Session = Depends(get_db)):
    """Create a new alert."""
    db_alert = Alert(
        alert_type=alert.alert_type,
        severity=alert.severity,
        title=alert.title,
        message=alert.message,
        segment_id=alert.segment_id,
        radius_km=alert.radius_km,
        status="active",
        delivery_channels=alert.delivery_channels or "in-app",
        source=alert.source or "manual",
        expires_at=alert.expires_at,
        timestamp=datetime.utcnow()
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.patch("/{alert_id}")
def update_alert_status(
    alert_id: int,
    status: str = Query(..., description="New status: active, acknowledged, resolved"),
    db: Session = Depends(get_db)
):
    """Update status of an alert."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = status
    db.commit()
    return {"message": "Alert status updated", "alert_id": alert_id, "status": status}
