"""Routing API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.routing.route_engine import RouteEngine
from app.schemas.routing import RouteRequest, RouteResponse

router = APIRouter()


@router.get("/", response_model=RouteResponse)
def calculate_route(
    from_node_id: int = Query(..., description="Starting node ID"),
    to_node_id: int = Query(..., description="Destination node ID"),
    mode: str = Query("balanced", description="Route mode: balanced, safest, or fastest"),
    db: Session = Depends(get_db)
):
    """Calculate optimal route between two nodes."""
    if mode not in ["balanced", "safest", "fastest"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode. Must be 'balanced', 'safest', or 'fastest'"
        )

    try:
        engine = RouteEngine(db)
        route = engine.find_route(from_node_id, to_node_id, mode)

        if not route:
            raise HTTPException(
                status_code=404,
                detail=f"No route found from node {from_node_id} to {to_node_id}"
            )

        return route

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Routing error: {str(e)}")
