"""Risk scoring API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List

from app.database import get_db
from app.models import RiskScore
from app.schemas.risk import RiskScoreOut

router = APIRouter()


@router.get("/scores", response_model=List[RiskScoreOut])
def get_risk_scores(
    segment_id: int = None,
    min_probability: float = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get risk scores for road segments."""
    query = db.query(RiskScore)

    if segment_id:
        query = query.filter(RiskScore.segment_id == segment_id)

    if min_probability:
        query = query.filter(RiskScore.risk_probability >= min_probability)

    # Get most recent score for each segment
    subquery = (
        db.query(
            RiskScore.segment_id,
            func.max(RiskScore.timestamp).label("max_timestamp")
        )
        .group_by(RiskScore.segment_id)
        .subquery()
    )

    scores = (
        query.join(
            subquery,
            and_(
                RiskScore.segment_id == subquery.c.segment_id,
                RiskScore.timestamp == subquery.c.max_timestamp
            )
        )
        .order_by(RiskScore.risk_probability.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return scores
