"""
Comprehensive Backend Test Suite for NER Smart Logistics Platform.
Tests all API endpoints, database operations, ML scoring, and routing engine.
"""
import sys
import os

# Add backend directory to sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    print("\n[1/8] Testing /health endpoint...")
    response = client.get("/health")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy"
    print(f"  PASS: Health check OK -> {data}")

def test_roads():
    print("\n[2/8] Testing /roads endpoints...")
    # List nodes
    res_nodes = client.get("/roads/nodes/")
    assert res_nodes.status_code == 200
    nodes = res_nodes.json()
    print(f"  PASS: Retrieved {len(nodes)} road nodes.")
    assert len(nodes) > 0

    # List segments
    res_segs = client.get("/roads/")
    assert res_segs.status_code == 200
    segs = res_segs.json()
    print(f"  PASS: Retrieved {len(segs)} road segments.")
    assert len(segs) > 0

    # Get single segment
    first_seg_id = segs[0]["id"]
    res_seg = client.get(f"/roads/{first_seg_id}")
    assert res_seg.status_code == 200
    seg = res_seg.json()
    print(f"  PASS: Retrieved segment {first_seg_id}: {seg['road_name']} ({seg['terrain']}, {seg['distance_km']} km)")

def test_vehicles():
    print("\n[3/8] Testing /vehicles endpoints...")
    # List vehicles
    res_v = client.get("/vehicles/")
    assert res_v.status_code == 200
    vehicles = res_v.json()
    print(f"  PASS: Retrieved {len(vehicles)} vehicles.")
    assert len(vehicles) > 0

    vid = vehicles[0]["id"]
    # Get vehicle details
    res_v_detail = client.get(f"/vehicles/{vid}")
    assert res_v_detail.status_code == 200
    v_data = res_v_detail.json()
    print(f"  PASS: Vehicle {vid} ({v_data['registration_number']}) details retrieved.")

    # Post GPS position
    pos_payload = {
        "vehicle_id": vid,
        "latitude": 26.0565,
        "longitude": 91.8205,
        "speed_kmh": 45.5,
        "heading": 180.0,
        "segment_id": 1,
        "is_synthetic": True
    }
    res_pos = client.post(f"/vehicles/{vid}/position", json=pos_payload)
    assert res_pos.status_code == 200
    print(f"  PASS: Ingested new GPS position for vehicle {vid}.")

    # Get vehicle positions history
    res_hist = client.get(f"/vehicles/{vid}/positions")
    assert res_hist.status_code == 200
    hist = res_hist.json()
    print(f"  PASS: Retrieved {len(hist)} position history records for vehicle {vid}.")

def test_weather():
    print("\n[4/8] Testing /weather endpoints...")
    # Ingest weather reading
    weather_payload = {
        "latitude": 26.1445,
        "longitude": 91.7362,
        "temperature_c": 24.5,
        "precipitation_mm": 12.0,
        "wind_speed_kmh": 15.0,
        "visibility_km": 8.0,
        "condition": "rain",
        "source": "openweathermap",
        "is_synthetic": True
    }
    res_ingest = client.post("/weather/ingest", json=weather_payload)
    assert res_ingest.status_code == 200
    print(f"  PASS: Successfully ingested weather reading.")

    # Get latest weather
    res_latest = client.get("/weather/latest?hours=24")
    assert res_latest.status_code == 200
    latest = res_latest.json()
    print(f"  PASS: Retrieved {len(latest)} recent weather readings.")

def test_risk_scores():
    print("\n[5/8] Testing /risk/scores endpoint...")
    res_risk = client.get("/risk/scores")
    assert res_risk.status_code == 200
    scores = res_risk.json()
    print(f"  PASS: Retrieved {len(scores)} segment risk scores.")
    if scores:
        top_risk = scores[0]
        print(f"  Top risk segment: #{top_risk['segment_id']}, Probability: {top_risk['risk_probability']:.4f}, Category: {top_risk['risk_category']}")

def test_routing():
    print("\n[6/8] Testing /route endpoint across modes (balanced, safest, fastest)...")
    res_segs = client.get("/roads/")
    segs = res_segs.json()

    # Pick from_node and to_node from the last corridor sequence
    last_seg = segs[-1]
    # Find start node of this corridor block
    # In our DB, sample segments run in sequence
    from_node = segs[0]["from_node_id"]
    to_node = segs[4]["to_node_id"] if len(segs) >= 5 else segs[-1]["to_node_id"]

    for mode in ["balanced", "safest", "fastest"]:
        res_route = client.get(f"/route?from_node_id={from_node}&to_node_id={to_node}&mode={mode}")
        assert res_route.status_code == 200, f"Mode {mode} failed: {res_route.text}"
        rdata = res_route.json()
        print(f"  PASS [{mode.upper()}]: Distance: {rdata['total_distance_km']} km, Time: {rdata['estimated_time_minutes']} min, Avg Risk: {rdata['average_risk']:.6f}, Nodes: {rdata['node_sequence']}")

def test_reports():
    print("\n[7/8] Testing /reports endpoints...")
    # List reports
    res_rep = client.get("/reports/")
    assert res_rep.status_code == 200
    reports = res_rep.json()
    print(f"  PASS: Retrieved {len(reports)} field reports.")

    # Create new report
    new_report = {
        "latitude": 25.9015,
        "longitude": 91.8797,
        "report_type": "landslide",
        "severity": "high",
        "description": "Debris blocking southbound lane near Nongpoh",
        "segment_id": 3,
        "reporter_id": "DRIVER_TEST_01"
    }
    res_create = client.post("/reports/", json=new_report)
    assert res_create.status_code == 200
    rep_obj = res_create.json()
    rep_id = rep_obj["id"]
    print(f"  PASS: Created report #{rep_id} ({rep_obj['report_type']}, severity: {rep_obj['severity']}).")

    # Update report status
    res_patch = client.patch(f"/reports/{rep_id}?status=verified")
    assert res_patch.status_code == 200
    updated_rep = res_patch.json()
    print(f"  PASS: Updated report #{rep_id} status to '{updated_rep['status']}'.")

def test_all():
    print("=" * 60)
    print("STARTING COMPLETE BACKEND VERIFICATION TEST")
    print("=" * 60)
    test_health()
    test_roads()
    test_vehicles()
    test_weather()
    test_risk_scores()
    test_routing()
    test_reports()
    print("\n" + "=" * 60)
    print("ALL 7 TEST SUITES PASSED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_all()
