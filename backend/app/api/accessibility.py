"""Accessibility scoring API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional

from app.database import get_db
from app.models import AccessibilityScore, RoadSegment
from app.schemas.accessibility import AccessibilityScoreOut

router = APIRouter()


@router.get("/scores", response_model=List[AccessibilityScoreOut])
def get_accessibility_scores(
    segment_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get accessibility scores for road segments."""
    query = db.query(AccessibilityScore)

    if segment_id:
        query = query.filter(AccessibilityScore.segment_id == segment_id)

    # Get most recent score for each segment
    subquery = (
        db.query(
            AccessibilityScore.segment_id,
            func.max(AccessibilityScore.timestamp).label("max_timestamp")
        )
        .group_by(AccessibilityScore.segment_id)
        .subquery()
    )

    scores = (
        query.join(
            subquery,
            and_(
                AccessibilityScore.segment_id == subquery.c.segment_id,
                AccessibilityScore.timestamp == subquery.c.max_timestamp
            )
        )
        .order_by(AccessibilityScore.accessibility_index.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # If no scores are recorded yet in DB, generate default scores from road segments dynamically
    if not scores:
        segments = db.query(RoadSegment).all()
        generated_scores = []
        for seg in segments:
            # Calculate synthetic baseline accessibility score
            base_index = 85.0 if seg.terrain == "flat" else (65.0 if seg.terrain == "hilly" else 45.0)
            score = AccessibilityScore(
                id=seg.id,
                segment_id=seg.id,
                accessibility_index=base_index,
                connectivity_score=80.0 if seg.terrain == "flat" else 55.0,
                alternative_routes_count=2 if seg.terrain == "flat" else 1,
                nearest_hospital_km=4.5 if seg.terrain == "flat" else 14.2,
                nearest_police_km=3.0 if seg.terrain == "flat" else 9.8,
                mobile_coverage="good" if seg.terrain == "flat" else "fair"
            )
            generated_scores.append(score)
        return generated_scores

    return scores
