"""Feature engineering for risk prediction."""
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict

from app.models import RoadSegment, DisruptionHistory, WeatherReading


def build_training_data(db: Session) -> pd.DataFrame:
    """
    Build training dataset for risk prediction.

    This function generates synthetic training data based on:
    1. Road segment characteristics (terrain, type)
    2. Historical disruption patterns
    3. Seasonal/weather patterns
    4. Time-based features

    Modeling assumptions (for synthetic data):
    - Monsoon season (June-Sept) has 3-5x higher disruption risk
    - Hilly/mountainous terrain has 4-8x higher landslide risk
    - Precipitation > 50mm/day significantly increases flooding risk
    - Historical disruptions on a segment increase future risk

    These assumptions are documented here so the pitch can cite them
    and so real data integration knows what to validate/replace.
    """
    segments = db.query(RoadSegment).all()

    # Generate per-segment-per-day features for past 365 days
    rows = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    for segment in segments:
        # Get historical disruptions for this segment
        disruptions = (
            db.query(DisruptionHistory)
            .filter(DisruptionHistory.segment_id == segment.id)
            .all()
        )

        current_date = start_date
        while current_date <= end_date:
            # Time-based features
            month = current_date.month
            is_monsoon = month in [6, 7, 8, 9]
            day_of_year = current_date.timetuple().tm_yday

            # Terrain features
            is_hilly = segment.terrain in ["hilly", "mountainous"]
            is_mountainous = segment.terrain == "mountainous"

            # Historical disruption count in past 90 days
            disruption_count = sum(
                1 for d in disruptions
                if (current_date - d.date).days <= 90 and d.date <= current_date
            )

            # Synthetic weather estimate (would be real weather data in production)
            # Monsoon months get higher precipitation
            estimated_precip = (
                30 + (month * 5) if is_monsoon else 5 + (month * 2)
            )

            # Target: did a disruption occur?
            had_disruption = any(
                d.date.date() == current_date.date()
                for d in disruptions
            )

            rows.append({
                'segment_id': segment.id,
                'date': current_date,
                'is_monsoon': int(is_monsoon),
                'is_hilly': int(is_hilly),
                'is_mountainous': int(is_mountainous),
                'month': month,
                'day_of_year': day_of_year,
                'recent_disruptions': disruption_count,
                'estimated_precipitation_mm': estimated_precip,
                'distance_km': segment.distance_km,
                'had_disruption': int(had_disruption)
            })

            current_date += timedelta(days=1)

    return pd.DataFrame(rows)


def extract_features_for_prediction(
    segment_id: int,
    current_date: datetime,
    db: Session,
    weather: Dict = None
) -> Dict:
    """
    Extract features for a single segment for real-time prediction.

    Args:
        segment_id: Road segment ID
        current_date: Current date/time
        db: Database session
        weather: Optional dict with current weather data

    Returns:
        Dict of features matching training data schema
    """
    segment = db.query(RoadSegment).filter(RoadSegment.id == segment_id).first()
    if not segment:
        raise ValueError(f"Segment {segment_id} not found")

    # Time features
    month = current_date.month
    is_monsoon = month in [6, 7, 8, 9]
    day_of_year = current_date.timetuple().tm_yday

    # Terrain features
    is_hilly = segment.terrain in ["hilly", "mountainous"]
    is_mountainous = segment.terrain == "mountainous"

    # Historical disruptions in past 90 days
    ninety_days_ago = current_date - timedelta(days=90)
    disruption_count = (
        db.query(DisruptionHistory)
        .filter(
            DisruptionHistory.segment_id == segment_id,
            DisruptionHistory.date >= ninety_days_ago,
            DisruptionHistory.date <= current_date
        )
        .count()
    )

    # Weather features
    if weather and 'precipitation_mm' in weather:
        precipitation = weather['precipitation_mm']
    else:
        # Fall back to seasonal estimate
        precipitation = 30 + (month * 5) if is_monsoon else 5 + (month * 2)

    return {
        'segment_id': segment_id,
        'is_monsoon': int(is_monsoon),
        'is_hilly': int(is_hilly),
        'is_mountainous': int(is_mountainous),
        'month': month,
        'day_of_year': day_of_year,
        'recent_disruptions': disruption_count,
        'estimated_precipitation_mm': precipitation,
        'distance_km': segment.distance_km
    }
