"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from app.config import settings
from app.api import roads, vehicles, weather, reports, risk, routing, alerts, accessibility

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered platform for intelligent urban transportation and logistics intelligence."
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(roads.router, prefix="/roads", tags=["roads"])
app.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(weather.router, prefix="/weather", tags=["weather"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(risk.router, prefix="/risk", tags=["risk"])
app.include_router(routing.router, prefix="/route", tags=["routing"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(accessibility.router, prefix="/accessibility", tags=["accessibility"])

# Static and HTML Dashboard serving
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DASHBOARD_FILE = BASE_DIR / "dashboard.html"
ROUTE_COMPARE_FILE = BASE_DIR / "route_comparison.html"


@app.get("/", response_class=HTMLResponse)
async def root_dashboard():
    """Serve the Command Center Web Dashboard directly at root."""
    if DASHBOARD_FILE.exists():
        return FileResponse(DASHBOARD_FILE)
    return {
        "message": "UrbanFlow AI API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_view():
    """Serve Web Dashboard."""
    if DASHBOARD_FILE.exists():
        return FileResponse(DASHBOARD_FILE)
    return {"message": "Dashboard file not found. Visit /docs for API documentation."}


@app.get("/comparison", response_class=HTMLResponse)
async def route_comparison_view():
    """Serve AI Route Comparison view."""
    if ROUTE_COMPARE_FILE.exists():
        return FileResponse(ROUTE_COMPARE_FILE)
    return {"message": "Route comparison file not found."}


@app.get("/api/info")
async def api_info():
    """API Info metadata."""
    return {
        "message": "UrbanFlow AI API",
        "version": settings.app_version,
        "docs": "/docs",
        "region": settings.default_city_name
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }
