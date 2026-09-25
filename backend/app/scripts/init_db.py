"""Initialize database tables."""
from sqlalchemy import text

from app.database import engine, Base
from app.config import settings
from app.models import (
    RoadNode, RoadSegment, Vehicle, VehiclePosition,
    WeatherReading, FieldReport, DisruptionHistory,
    RiskScore, AccessibilityScore, Alert
)


def init_db():
    """Create all database tables."""
    print("Initializing database...")

    # Enable PostGIS extension if running PostgreSQL
    if "postgres" in str(engine.url).lower():
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
            conn.commit()
            print("[OK] PostGIS extension enabled (PostgreSQL mode)")
    else:
        print(f"[OK] SQLite database mode active: {settings.database_url}")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("[OK] All tables created successfully")

    print("\nDatabase tables:")
    print("  - road_nodes")
    print("  - road_segments")
    print("  - vehicles")
    print("  - vehicle_positions")
    print("  - weather_readings")
    print("  - field_reports")
    print("  - disruption_history")
    print("  - risk_scores")
    print("  - accessibility_scores")
    print("  - alerts")
    print("\n[OK] Database initialization complete!")


if __name__ == "__main__":
    init_db()
