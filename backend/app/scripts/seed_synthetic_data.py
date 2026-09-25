"""Seed synthetic data for development and testing."""
import random
from datetime import datetime, timedelta
from geoalchemy2.elements import WKTElement

from app.database import SessionLocal
from app.models import Vehicle, RoadSegment, DisruptionHistory


def seed_synthetic_data():
    """
    Seed database with synthetic vehicles and historical disruption data.

    This creates:
    1. Sample vehicles for GPS tracking simulation
    2. Historical disruption events for ML training

    All data is flagged as synthetic (is_synthetic=True).
    """
    print("Seeding synthetic data...")
    db = SessionLocal()

    try:
        # Create sample vehicles
        vehicles_data = [
            {"reg": "AS-01-1234", "type": "truck", "operator": "NER Logistics Ltd"},
            {"reg": "AS-01-5678", "type": "truck", "operator": "Shillong Transport Co"},
            {"reg": "ML-05-9012", "type": "bus", "operator": "Meghalaya State Transport"},
            {"reg": "AS-01-3456", "type": "truck", "operator": "NER Logistics Ltd"},
        ]

        vehicles = []
        for data in vehicles_data:
            vehicle = Vehicle(
                registration_number=data["reg"],
                vehicle_type=data["type"],
                operator=data["operator"],
                is_active=True,
                is_synthetic=True
            )
            db.add(vehicle)
            vehicles.append(vehicle)

        db.commit()
        print(f"[OK] Created {len(vehicles)} vehicles")

        # Generate synthetic disruption history for ML training
        segments = db.query(RoadSegment).all()
        print(f"Generating disruption history for {len(segments)} segments...")

        disruptions = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)  # 2 years of history

        disruption_types = [
            "landslide", "flooding", "accident", "roadwork", "debris"
        ]

        for segment in segments:
            # Risk factors based on terrain
            base_risk = {
                "flat": 0.002,        # 0.2% daily risk
                "hilly": 0.008,       # 0.8% daily risk
                "mountainous": 0.015  # 1.5% daily risk
            }.get(segment.terrain, 0.005)

            current_date = start_date
            while current_date <= end_date:
                month = current_date.month
                is_monsoon = month in [6, 7, 8, 9]

                # Monsoon season multiplier
                daily_risk = base_risk * 3.5 if is_monsoon else base_risk

                # Random disruption based on risk
                if random.random() < daily_risk:
                    # Determine disruption type (terrain-dependent)
                    if segment.terrain == "mountainous":
                        disruption_type = random.choice(["landslide", "landslide", "rockfall", "accident"])
                    elif segment.terrain == "hilly":
                        disruption_type = random.choice(["landslide", "flooding", "accident"])
                    else:
                        disruption_type = random.choice(["flooding", "accident", "roadwork"])

                    severity = random.choice(["low", "low", "medium", "medium", "high"])
                    duration = random.uniform(2, 48) if severity != "low" else random.uniform(0.5, 4)

                    # Synthetic precipitation
                    precip = random.uniform(50, 150) if is_monsoon else random.uniform(0, 30)
                    temp = random.uniform(20, 30)

                    disruption = DisruptionHistory(
                        segment_id=segment.id,
                        date=current_date,
                        disruption_type=disruption_type,
                        severity=severity,
                        duration_hours=duration,
                        was_monsoon=is_monsoon,
                        precipitation_mm=precip,
                        temperature_c=temp,
                        is_synthetic=True,
                        source="synthetic_generator"
                    )
                    db.add(disruption)
                    disruptions.append(disruption)

                current_date += timedelta(days=1)

        db.commit()
        print(f"[OK] Generated {len(disruptions)} synthetic disruption events")

        # Print summary by terrain
        print("\n" + "="*60)
        print("SYNTHETIC DATA SEEDING COMPLETE")
        print("="*60)

        print(f"\nVehicles: {len(vehicles)}")
        for v in vehicles:
            print(f"  - {v.registration_number} ({v.vehicle_type})")

        print(f"\nDisruption Events: {len(disruptions)}")
        for terrain in ["flat", "hilly", "mountainous"]:
            count = sum(1 for d in disruptions if
                       db.query(RoadSegment).filter(RoadSegment.id == d.segment_id).first().terrain == terrain)
            print(f"  - {terrain:12}: {count:4} events")

        disruption_rate = len(disruptions) / (len(segments) * 730)
        print(f"\nOverall disruption rate: {disruption_rate:.2%} per segment-day")
        print("\n[OK] Synthetic data seeding complete!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_synthetic_data()
