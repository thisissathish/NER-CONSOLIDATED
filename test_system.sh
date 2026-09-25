# Testing & Verification Commands
# Run these to verify your system before demo

echo "=========================================="
echo "NER Smart Logistics Platform - System Check"
echo "=========================================="

# 1. Check API Health
echo ""
echo "1. Checking API health..."
curl -s http://localhost:8000/health | python -m json.tool

# 2. Check Risk Scores
echo ""
echo "2. Checking risk scores (top 3)..."
curl -s http://localhost:8000/risk/scores | python -m json.tool | head -60

# 3. Check Vehicles
echo ""
echo "3. Checking active vehicles..."
curl -s http://localhost:8000/vehicles | python -m json.tool

# 4. Check Roads
echo ""
echo "4. Checking road segments (first 2)..."
curl -s http://localhost:8000/roads | python -m json.tool | head -40

# 5. Test Route Optimization
echo ""
echo "5. Testing route optimization (Guwahati to Shillong)..."
# Get node IDs from roads first
FIRST_NODE=$(curl -s http://localhost:8000/roads | python -c "import sys, json; roads=json.load(sys.stdin); print(roads[0]['from_node_id'] if roads else 7)")
LAST_NODE=$(curl -s http://localhost:8000/roads | python -c "import sys, json; roads=json.load(sys.stdin); print(roads[-1]['to_node_id'] if roads else 12)")

echo "  From node: $FIRST_NODE, To node: $LAST_NODE"
curl -s "http://localhost:8000/route?from_node_id=${FIRST_NODE}&to_node_id=${LAST_NODE}&mode=balanced" | python -m json.tool | head -50

# 6. Check Field Reports
echo ""
echo "6. Checking field reports..."
curl -s http://localhost:8000/reports/ | python -m json.tool | head -30

echo ""
echo "=========================================="
echo "System check complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Open dashboard.html in browser"
echo "2. Open route_comparison.html in browser"
echo "3. Take screenshots of both"
echo "4. Practice demo script 3 times"
echo ""
