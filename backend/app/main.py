"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import roads, vehicles, weather, reports, risk, routing

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-Based Smart Logistics Platform for North Eastern Region"
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


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "NER Smart Logistics Platform API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }
