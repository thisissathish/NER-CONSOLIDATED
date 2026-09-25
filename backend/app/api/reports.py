"""Field reports API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db, make_point
from app.models import FieldReport
from app.schemas.report import FieldReportIn, FieldReportOut

router = APIRouter()


@router.get("/", response_model=List[FieldReportOut])
def list_reports(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List field reports."""
    query = db.query(FieldReport)
    if status:
        query = query.filter(FieldReport.status == status)
    reports = query.order_by(FieldReport.timestamp.desc()).offset(skip).limit(limit).all()
    return reports


@router.post("/", response_model=FieldReportOut)
def create_report(report: FieldReportIn, db: Session = Depends(get_db)):
    """Submit a field report."""
    db_report = FieldReport(
        latitude=report.latitude,
        longitude=report.longitude,
        location=make_point(report.longitude, report.latitude),
        timestamp=datetime.utcnow(),
        report_type=report.report_type,
        severity=report.severity,
        description=report.description,
        segment_id=report.segment_id,
        reporter_id=report.reporter_id,
        status="active",
        is_verified=False
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


@router.patch("/{report_id}")
def update_report_status(
    report_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update report status."""
    report = db.query(FieldReport).filter(FieldReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.status = status
    db.commit()
    return {"message": "Status updated", "report_id": report_id, "status": status}
