"""Load sample road network for Guwahati-Shillong corridor."""
from app.database import SessionLocal, make_point, make_linestring
from app.models import RoadNode, RoadSegment


def load_sample_roads():
    """
    Load placeholder road network for Guwahati-Shillong corridor.
    Route: Guwahati -> Jorabat -> Byrnihat -> Nongpoh -> Umsning -> Shillong
    """
    print("Loading sample road network...")
    db = SessionLocal()

    try:
        # Define nodes along the corridor
        nodes_data = [
            {"name": "Guwahati", "lat": 26.1445, "lon": 91.7362, "type": "town"},
            {"name": "Jorabat", "lat": 26.0565, "lon": 91.8205, "type": "junction"},
            {"name": "Byrnihat", "lat": 25.9932, "lon": 91.9119, "type": "waypoint"},
            {"name": "Nongpoh", "lat": 25.9015, "lon": 91.8797, "type": "town"},
            {"name": "Umsning", "lat": 25.8655, "lon": 91.7852, "type": "waypoint"},
            {"name": "Shillong", "lat": 25.5788, "lon": 91.8933, "type": "town"},
        ]

        nodes = []
        for data in nodes_data:
            node = RoadNode(
                name=data["name"],
                latitude=data["lat"],
                longitude=data["lon"],
                location=make_point(data["lon"], data["lat"]),
                node_type=data["type"],
                is_synthetic=True
            )
            db.add(node)
            nodes.append(node)

        db.commit()
        print(f"[OK] Created {len(nodes)} nodes")

        # Refresh to get IDs
        for node in nodes:
            db.refresh(node)

        # Define segments
        segments_data = [
            {
                "from": "Guwahati", "to": "Jorabat",
                "distance": 22.5, "terrain": "flat", "road": "NH40"
            },
            {
                "from": "Jorabat", "to": "Byrnihat",
                "distance": 15.8, "terrain": "flat", "road": "NH40"
            },
            {
                "from": "Byrnihat", "to": "Nongpoh",
                "distance": 18.3, "terrain": "hilly", "road": "NH40"
            },
            {
                "from": "Nongpoh", "to": "Umsning",
                "distance": 14.2, "terrain": "hilly", "road": "NH40"
            },
            {
                "from": "Umsning", "to": "Shillong",
                "distance": 32.7, "terrain": "mountainous", "road": "NH40"
            },
        ]

        node_map = {node.name: node for node in nodes}
        segments = []

        for data in segments_data:
            from_node = node_map[data["from"]]
            to_node = node_map[data["to"]]

            linestring_wkt = (
                f"LINESTRING({from_node.longitude} {from_node.latitude}, "
                f"{to_node.longitude} {to_node.latitude})"
            )

            segment = RoadSegment(
                from_node_id=from_node.id,
                to_node_id=to_node.id,
                distance_km=data["distance"],
                road_name=data["road"],
                road_type="highway",
                terrain=data["terrain"],
                geometry=make_linestring(linestring_wkt),
                is_synthetic=True
            )
            db.add(segment)
            segments.append(segment)

        db.commit()
        print(f"[OK] Created {len(segments)} segments")

        print("\n" + "="*60)
        print("SAMPLE ROAD NETWORK LOADED")
        print("="*60)
        print("\nGuwahati -> Shillong Corridor (NH40)")
        print("-" * 60)

        total_distance = 0
        for seg_data in segments_data:
            print(f"{seg_data['from']:15} -> {seg_data['to']:15} "
                  f"{seg_data['distance']:6.1f} km  ({seg_data['terrain']})")
            total_distance += seg_data['distance']

        print("-" * 60)
        print(f"Total distance: {total_distance:.1f} km")
        print("\n[OK] Sample road network loaded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    load_sample_roads()
