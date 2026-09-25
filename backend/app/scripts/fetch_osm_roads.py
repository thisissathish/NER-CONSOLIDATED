"""Fetch real road network data from OpenStreetMap."""
import osmnx as ox
ox.settings.useful_tags_node = []
ox.settings.useful_tags_way = []
ox.settings.overpass_url = "https://overpass.kumi.systems/api/interpreter"
from geoalchemy2.elements import WKTElement

from app.database import SessionLocal
from app.models import RoadNode, RoadSegment
from app.config import settings


def fetch_osm_roads():
    """
    Fetch real road network from OpenStreetMap for Guwahati-Shillong corridor.

    This replaces the placeholder 6-node network with real OSM data including
    actual intersections, alternate routes, and precise geometries.

    Requirements:
    - Internet connection
    - osmnx library
    - Sufficient time for API calls (~2-5 minutes)
    """
    print("Fetching road network from OpenStreetMap...")
    print("This may take 2-5 minutes...\n")

    # Define bounding box for corridor
    bbox = (
        settings.corridor_min_lat,
        settings.corridor_max_lat,
        settings.corridor_min_lon,
        settings.corridor_max_lon
    )

    print(f"Bounding box: {bbox}")

    try:
        # Fetch road network
        print("Downloading from Overpass API...")
        G = ox.graph_from_bbox(
            (bbox[1], bbox[0], bbox[3], bbox[2]),
            network_type='drive',
            simplify=True
        )

        print(f"[OK] Downloaded {len(G.nodes)} nodes and {len(G.edges)} edges")

        # Convert to undirected for simpler processing
        G = ox.get_undirected(G)

        db = SessionLocal()

        try:
            # Clear existing road data
            print("\nClearing existing road data...")
            db.query(RoadSegment).delete()
            db.query(RoadNode).delete()
            db.commit()
            print("[OK] Cleared old data")

            # Insert nodes
            print("\nInserting nodes...")
            node_id_map = {}  # OSM ID -> DB ID

            for osm_id, data in G.nodes(data=True):
                lat = data['y']
                lon = data['x']
                location = WKTElement(f"POINT({lon} {lat})", srid=4326)

                node = RoadNode(
                    name=f"Node_{osm_id}",
                    latitude=lat,
                    longitude=lon,
                    location=location,
                    node_type="junction",
                    is_synthetic=False
                )
                db.add(node)
                db.flush()
                node_id_map[osm_id] = node.id

            print(f"[OK] Inserted {len(node_id_map)} nodes")

            # Insert segments
            print("\nInserting segments...")
            segment_count = 0

            for u, v, data in G.edges(data=True):
                from_node_id = node_id_map[u]
                to_node_id = node_id_map[v]

                # Calculate distance
                distance_m = data.get('length', 0)
                distance_km = distance_m / 1000.0

                # Determine terrain (simplified - would need elevation data for accuracy)
                terrain = "flat"  # Default

                # Road type
                road_type = data.get('highway', 'unclassified')
                if road_type in ['motorway', 'trunk', 'primary']:
                    road_type_clean = 'highway'
                elif road_type in ['secondary', 'tertiary']:
                    road_type_clean = 'arterial'
                else:
                    road_type_clean = 'collector'

                # Road name
                road_name = data.get('name', f"Road {u}-{v}")

                # Geometry
                if 'geometry' in data:
                    # Use OSM geometry
                    coords = list(data['geometry'].coords)
                    linestring = "LINESTRING(" + ", ".join(f"{c[0]} {c[1]}" for c in coords) + ")"
                else:
                    # Simple straight line
                    from_node = G.nodes[u]
                    to_node = G.nodes[v]
                    linestring = f"LINESTRING({from_node['x']} {from_node['y']}, {to_node['x']} {to_node['y']})"

                geometry = WKTElement(linestring, srid=4326)

                segment = RoadSegment(
                    from_node_id=from_node_id,
                    to_node_id=to_node_id,
                    distance_km=distance_km,
                    road_name=road_name,
                    road_type=road_type_clean,
                    terrain=terrain,
                    geometry=geometry,
                    is_synthetic=False
                )
                db.add(segment)
                segment_count += 1

            db.commit()
            print(f"[OK] Inserted {segment_count} segments")

            print("\n" + "="*60)
            print("OSM DATA IMPORT COMPLETE")
            print("="*60)
            print(f"\nNodes: {len(node_id_map)}")
            print(f"Segments: {segment_count}")
            print("\n[OK] Real OpenStreetMap data loaded successfully!")
            print("\nNext steps:")
            print("  1. Run: python -m app.scripts.seed_synthetic_data")
            print("  2. Run: python -m app.ml.train_risk_model")
            print("  3. Run: python -m app.ml.score_segments")

        finally:
            db.close()

    except Exception as e:
        print(f"\n✗ Error fetching OSM data: {str(e)}")
        print("\nPossible causes:")
        print("  - No internet connection")
        print("  - Overpass API timeout")
        print("  - Invalid bounding box")
        print("\nFalling back to sample data. Run load_sample_roads.py instead.")


if __name__ == "__main__":
    fetch_osm_roads()
