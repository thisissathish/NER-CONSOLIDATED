"""Graph builder for road network."""
import networkx as nx
from sqlalchemy.orm import Session
from typing import Dict, Tuple

from app.models import RoadNode, RoadSegment, RiskScore


class GraphBuilder:
    """Builds a NetworkX graph from the road network database."""

    def __init__(self, db: Session):
        self.db = db
        self.graph = nx.DiGraph()

    def build_graph(self) -> nx.DiGraph:
        """Build a directed graph from road segments."""
        # Add all nodes
        nodes = self.db.query(RoadNode).all()
        for node in nodes:
            self.graph.add_node(
                node.id,
                name=node.name,
                latitude=node.latitude,
                longitude=node.longitude,
                node_type=node.node_type
            )

        # Add all edges (segments)
        segments = self.db.query(RoadSegment).all()
        for segment in segments:
            # Get latest risk score for this segment
            risk = (
                self.db.query(RiskScore)
                .filter(RiskScore.segment_id == segment.id)
                .order_by(RiskScore.timestamp.desc())
                .first()
            )

            risk_probability = risk.risk_probability if risk else 0.01

            # Add bidirectional edges (roads can be traveled both ways)
            for from_id, to_id in [(segment.from_node_id, segment.to_node_id),
                                    (segment.to_node_id, segment.from_node_id)]:
                self.graph.add_edge(
                    from_id,
                    to_id,
                    segment_id=segment.id,
                    distance_km=segment.distance_km,
                    road_name=segment.road_name,
                    terrain=segment.terrain,
                    risk_probability=risk_probability
                )

        return self.graph

    def get_risk_weights(self) -> Dict[Tuple[int, int], float]:
        """Get risk-based weights for all edges."""
        weights = {}
        for u, v, data in self.graph.edges(data=True):
            # Higher risk = higher weight (less preferred)
            weights[(u, v)] = data['risk_probability']
        return weights

    def get_distance_weights(self) -> Dict[Tuple[int, int], float]:
        """Get distance-based weights for all edges."""
        weights = {}
        for u, v, data in self.graph.edges(data=True):
            weights[(u, v)] = data['distance_km']
        return weights
