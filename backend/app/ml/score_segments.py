"""Score all road segments with ML risk model."""
import pickle
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import RoadSegment, RiskScore, WeatherReading
from app.ml.features import extract_features_for_prediction


def load_model():
    """Load trained risk model."""
    model_path = Path(__file__).parent.parent.parent / 'models' / 'risk_model.pkl'
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. "
            "Run 'python -m app.ml.train_risk_model' first."
        )

    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)

    return model_data


def get_recent_weather(db: Session, hours: int = 6):
    """Get recent weather readings."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    readings = (
        db.query(WeatherReading)
        .filter(WeatherReading.timestamp >= cutoff)
        .order_by(WeatherReading.timestamp.desc())
        .all()
    )

    if not readings:
        return None

    # Average recent readings
    return {
        'precipitation_mm': sum(r.precipitation_mm or 0 for r in readings) / len(readings),
        'temperature_c': sum(r.temperature_c or 0 for r in readings) / len(readings),
        'wind_speed_kmh': sum(r.wind_speed_kmh or 0 for r in readings) / len(readings)
    }


def categorize_risk(probability: float) -> str:
    """Categorize risk probability into levels."""
    if probability < 0.01:
        return "low"
    elif probability < 0.03:
        return "medium"
    elif probability < 0.06:
        return "high"
    else:
        return "critical"


def score_all_segments():
    """Score all road segments with current risk."""
    print("Loading risk model...")
    model_data = load_model()
    model = model_data['model']
    feature_cols = model_data['feature_cols']
    version = model_data['version']

    print(f"Model version: {version}")
    print(f"Trained at: {model_data['trained_at']}")

    db = SessionLocal()

    try:
        # Get current weather
        print("\nFetching recent weather...")
        weather = get_recent_weather(db)
        if weather:
            print(f"Using weather: {weather['precipitation_mm']:.1f}mm precip")
        else:
            print("No recent weather data, using seasonal estimates")

        # Get all segments
        segments = db.query(RoadSegment).all()
        print(f"\nScoring {len(segments)} segments...")

        current_time = datetime.utcnow()
        scores = []

        for segment in segments:
            # Extract features
            features = extract_features_for_prediction(
                segment.id,
                current_time,
                db,
                weather
            )

            # Predict
            X = pd.DataFrame([features])[feature_cols]
            risk_prob = float(model.predict_proba(X)[0, 1])  # Convert numpy.float32 to Python float

            # Save risk score
            risk_score = RiskScore(
                segment_id=segment.id,
                timestamp=current_time,
                risk_probability=risk_prob,
                risk_category=categorize_risk(risk_prob),
                weather_factor=float(features.get('estimated_precipitation_mm', 0)) / 100,
                terrain_factor=float(features.get('is_hilly', 0) + features.get('is_mountainous', 0)),
                historical_factor=float(features.get('recent_disruptions', 0)) / 10,
                model_version=version,
                confidence=0.85  # Would be computed from model uncertainty in production
            )
            db.add(risk_score)
            scores.append((segment.id, risk_prob, segment.from_node.name, segment.to_node.name))

        db.commit()

        # Print summary
        print("\n" + "="*70)
        print("RISK SCORING COMPLETE")
        print("="*70)
        print(f"\nSegment Risk Rankings:")
        print(f"{'ID':<5} {'From':<20} {'To':<20} {'Risk %':<10}")
        print("-" * 70)

        for seg_id, risk, from_name, to_name in sorted(scores, key=lambda x: x[1], reverse=True):
            print(f"{seg_id:<5} {from_name:<20} {to_name:<20} {risk*100:>6.2f}%")

        avg_risk = sum(s[1] for s in scores) / len(scores)
        max_risk = max(s[1] for s in scores)

        print("-" * 70)
        print(f"Average risk: {avg_risk*100:.2f}%")
        print(f"Maximum risk: {max_risk*100:.2f}%")
        print(f"\n[OK] {len(scores)} segments scored and saved to database")

    finally:
        db.close()


if __name__ == "__main__":
    score_all_segments()
