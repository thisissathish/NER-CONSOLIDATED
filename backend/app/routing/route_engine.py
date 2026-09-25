"""Route calculation engine."""
import networkx as nx
from sqlalchemy.orm import Session
from typing import List, Optional

from app.routing.graph_builder import GraphBuilder
from app.schemas.routing import RouteResponse, RouteSegmentInfo


class RouteEngine:
    """Calculate optimal routes based on different strategies."""

    def __init__(self, db: Session):
        self.db = db
        builder = GraphBuilder(db)
        self.graph = builder.build_graph()

    def find_route(
        self,
        from_node_id: int,
        to_node_id: int,
        mode: str = "balanced"
    ) -> Optional[RouteResponse]:
        """
        Find optimal route between two nodes.

        Args:
            from_node_id: Starting node ID
            to_node_id: Destination node ID
            mode: Route optimization mode
                - "balanced": Balance distance and risk
                - "safest": Minimize risk (may be longer)
                - "fastest": Minimize distance (may be riskier)

        Returns:
            RouteResponse with path details or None if no route exists
        """
        if from_node_id not in self.graph or to_node_id not in self.graph:
            raise ValueError(f"Invalid node IDs: {from_node_id} or {to_node_id}")

        # Calculate weight for each edge based on mode
        weight_attr = self._get_weight_attribute(mode)

        try:
            # Find shortest path using the selected weight
            path = nx.shortest_path(
                self.graph,
                source=from_node_id,
                target=to_node_id,
                weight=weight_attr
            )

            return self._build_route_response(path, mode)

        except nx.NetworkXNoPath:
            return None

    def _get_weight_attribute(self, mode: str) -> str:
        """
        Determine weight attribute for pathfinding.

        For now, all modes use a composite weight since we need to
        compute it dynamically. In a production system with alternate
        routes, this would differentiate between modes.
        """
        # Pre-compute composite weights based on mode
        for u, v, data in self.graph.edges(data=True):
            distance = data['distance_km']
            risk = data['risk_probability']

            if mode == "fastest":
                # Minimize distance, slight risk penalty
                data['weight'] = distance + (risk * 5)
            elif mode == "safest":
                # Heavily penalize risk
                data['weight'] = (risk * 100) + distance
            else:  # balanced
                # Equal weight to distance and risk
                data['weight'] = distance + (risk * 50)

        return 'weight'

    def _build_route_response(
        self,
        path: List[int],
        mode: str
    ) -> RouteResponse:
        """Build route response from node path."""
        segments = []
        total_distance = 0.0
        risk_values = []

        # Build segment information
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            edge_data = self.graph[from_node][to_node]

            distance = edge_data['distance_km']
            risk = edge_data['risk_probability']

            segments.append(RouteSegmentInfo(
                segment_id=edge_data['segment_id'],
                from_node_id=from_node,
                to_node_id=to_node,
                distance_km=distance,
                risk_probability=risk,
                estimated_time_minutes=distance * 1.2  # ~50 km/h average
            ))

            total_distance += distance
            risk_values.append(risk)

        # Calculate summary statistics
        avg_risk = sum(risk_values) / len(risk_values) if risk_values else 0.0
        max_risk = max(risk_values) if risk_values else 0.0
        estimated_time = total_distance * 1.2  # ~50 km/h average speed

        return RouteResponse(
            from_node_id=path[0],
            to_node_id=path[-1],
            mode=mode,
            total_distance_km=round(total_distance, 2),
            estimated_time_minutes=round(estimated_time, 1),
            average_risk=round(avg_risk, 4),
            max_risk=round(max_risk, 4),
            segments=segments,
            node_sequence=path
        )
