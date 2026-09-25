"""Database connection, session management, and geometry helpers."""
from sqlalchemy import create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Configure SQLite vs PostgreSQL connection options
is_sqlite = settings.database_url.startswith("sqlite")

connect_args = {}
if is_sqlite:
    connect_args["check_same_thread"] = False

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=not is_sqlite,
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_geom_type(geom_type: str = "POINT", srid: int = 4326):
    """
    Return appropriate column type for geometry.
    Uses String for SQLite (Zero-Docker mode) and GeoAlchemy2 Geometry for PostgreSQL/PostGIS.
    """
    if is_sqlite:
        return String(255)
    try:
        from geoalchemy2 import Geometry
        return Geometry(geom_type, srid=srid)
    except Exception:
        return String(255)


def make_point(lon: float, lat: float):
    """Create point geometry compatible with SQLite and PostGIS."""
    if is_sqlite:
        return f"POINT({lon} {lat})"
    try:
        from geoalchemy2.elements import WKTElement
        return WKTElement(f"POINT({lon} {lat})", srid=4326)
    except Exception:
        return f"POINT({lon} {lat})"


def make_linestring(coords_wkt: str):
    """Create linestring geometry compatible with SQLite and PostGIS."""
    if is_sqlite:
        return coords_wkt
    try:
        from geoalchemy2.elements import WKTElement
        return WKTElement(coords_wkt, srid=4326)
    except Exception:
        return coords_wkt
