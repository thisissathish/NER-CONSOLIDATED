"""Simulate GPS updates for vehicles."""
import time
import random
from datetime import datetime

import httpx
from sqlalchemy import func

from app.database import SessionLocal
from app.models import Vehicle, RoadSegment, RoadNode


def simulate_gps():
    """
    Simulate vehicle GPS updates along the road network.

    Moves vehicles along road segments and posts position updates
    to the API endpoint. Runs continuously until stopped.
    """
    print("Starting GPS simulation...")
    print("Press Ctrl+C to stop\n")

    db = SessionLocal()
    api_url = "http://localhost:8000"

    try:
        # Get all active vehicles
        vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).all()
        if not vehicles:
            print("No active vehicles found. Run seed_synthetic_data.py first.")
            return

        print(f"Tracking {len(vehicles)} vehicles")

        # Initialize vehicle positions
        vehicle_positions = {}
        for vehicle in vehicles:
            # Start at random segment
            segment = db.query(RoadSegment).order_by(func.random()).first()
            vehicle_positions[vehicle.id] = {
                "segment_id": segment.id,
                "progress": 0.0  # 0.0 to 1.0 along segment
            }

        iteration = 0
        while True:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")

            for vehicle in vehicles:
                pos = vehicle_positions[vehicle.id]
                segment = db.query(RoadSegment).filter(RoadSegment.id == pos["segment_id"]).first()

                # Get nodes
                from_node = segment.from_node
                to_node = segment.to_node

                # Interpolate position along segment
                lat = from_node.latitude + (to_node.latitude - from_node.latitude) * pos["progress"]
                lon = from_node.longitude + (to_node.longitude - from_node.longitude) * pos["progress"]

                # Calculate speed and heading
                speed = random.uniform(40, 65)  # km/h
                heading = random.uniform(0, 360)

                # Post position update
                try:
                    response = httpx.post(
                        f"{api_url}/vehicles/{vehicle.id}/position",
                        json={
                            "latitude": lat,
                            "longitude": lon,
                            "speed_kmh": speed,
                            "heading": heading,
                            "segment_id": segment.id
                        },
                        timeout=5.0
                    )
                    if response.status_code == 200:
                        print(f"[OK] {vehicle.registration_number}: {from_node.name} -> {to_node.name} "
                              f"({pos['progress']*100:.0f}%) @ {speed:.0f} km/h")
                    else:
                        print(f"✗ {vehicle.registration_number}: API error {response.status_code}")

                except Exception as e:
                    print(f"✗ {vehicle.registration_number}: {str(e)}")

                # Advance position (roughly 1km per update at 50 km/h)
                pos["progress"] += 1.0 / segment.distance_km

                # Move to next segment if completed
                if pos["progress"] >= 1.0:
                    # Find next segment (random choice of outgoing segments)
                    next_segments = (
                        db.query(RoadSegment)
                        .filter(RoadSegment.from_node_id == segment.to_node_id)
                        .all()
                    )

                    if next_segments:
                        next_segment = random.choice(next_segments)
                        pos["segment_id"] = next_segment.id
                        pos["progress"] = 0.0
                        print(f"  -> {vehicle.registration_number} entered segment {next_segment.id}")
                    else:
                        # Dead end, reverse direction
                        pos["progress"] = 0.0
                        print(f"  -> {vehicle.registration_number} turned around")

            # Wait before next update
            time.sleep(5)  # 5 second intervals

    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user")
    finally:
        db.close()


if __name__ == "__main__":
    simulate_gps()
