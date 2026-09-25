#!/bin/bash
# Demo Disruption Scenarios for NER Smart Logistics
# Run this to populate realistic field reports for presentation

API_BASE="http://localhost:8000"

echo "=========================================="
echo "Adding demo disruption scenarios..."
echo "=========================================="

# Scenario 1: Critical Landslide (High Risk)
echo "Scenario 1: Landslide at Nongpoh (Critical)..."
curl -X POST "$API_BASE/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "landslide",
    "severity": "critical",
    "description": "NH40 completely blocked by landslide near Nongpoh. Massive boulders on road. Traffic diverted via alternate route. Heavy rainfall continuing.",
    "latitude": 25.9015,
    "longitude": 91.8797,
    "reporter_id": "HPO_NGL_001"
  }' > /dev/null && echo "  ✓ Added"

# Scenario 2: Weather Warning (High Risk)
echo "Scenario 2: Heavy rainfall warning at Shillong..."
curl -X POST "$API_BASE/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "weather_warning",
    "severity": "high",
    "description": "IMD Red Alert: Very heavy rainfall expected in Meghalaya. Visibility <100m in some areas. Advise caution on NH40 Shillong section.",
    "latitude": 25.5788,
    "longitude": 91.8933,
    "reporter_id": "IMD_SHL_001"
  }' > /dev/null && echo "  ✓ Added"

# Scenario 3: Road Construction (Medium Risk)
echo "Scenario 3: Road widening work at Jorabat..."
curl -X POST "$API_BASE/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "construction",
    "severity": "medium",
    "description": "NH40 widening work in progress near Jorabat. Single lane open. Expect 20-30 min delays during peak hours. Expected completion: Oct 15.",
    "latitude": 26.0565,
    "longitude": 91.8205,
    "reporter_id": "PWD_ASS_002"
  }' > /dev/null && echo "  ✓ Added"

# Scenario 4: Accident Cleared (Low Risk - Positive Update)
echo "Scenario 4: Accident resolved at Byrnihat..."
curl -X POST "$API_BASE/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "accident_cleared",
    "severity": "low",
    "description": "Earlier collision at Byrnihat junction cleared. Both vehicles towed. All lanes open. Traffic moving normally.",
    "latitude": 25.9932,
    "longitude": 91.9119,
    "reporter_id": "TC_BYR_001"
  }' > /dev/null && echo "  ✓ Added"

# Scenario 5: Congestion Update (Medium Risk)
echo "Scenario 5: Congestion at Guwahati entry..."
curl -X POST "$API_BASE/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "congestion",
    "severity": "medium",
    "description": "Heavy traffic at Guwahati NH40 entry point. Local traffic jam due to market day. Expect 45 min delay. Use bypass route via AG Road.",
    "latitude": 26.1445,
    "longitude": 91.7362,
    "reporter_id": "TC_GHT_001"
  }' > /dev/null && echo "  ✓ Added"

# Scenario 6: Flooding Risk (High Risk - Seasonal)
echo "Scenario 6: Waterlogging at Umsning..."
curl -X POST "$API_BASE/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "weather_warning",
    "severity": "high",
    "description": "Waterlogging reported at Umsning junction due to poor drainage. Water level rising. Vehicles proceeding with caution. Pumping underway.",
    "latitude": 25.8655,
    "longitude": 91.7852,
    "reporter_id": "PWD_MGL_001"
  }' > /dev/null && echo "  ✓ Added"

echo ""
echo "=========================================="
echo "Demo scenarios added successfully!"
echo "=========================================="
echo ""
echo "To verify, run:"
echo "  curl http://localhost:8000/reports | python -m json.tool"
echo ""
