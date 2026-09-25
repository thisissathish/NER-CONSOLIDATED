# NER Smart Logistics Platform - Backend

FastAPI backend for the NER Smart Logistics Platform, providing AI-powered route optimization, real-time vehicle tracking, and risk assessment for the Guwahati–Shillong corridor.

## Features

- **Road Network Management**: Store and query road segments with PostGIS
- **Vehicle Tracking**: Real-time GPS position ingestion and history
- **Weather Integration**: OpenWeatherMap API integration
- **Risk Prediction**: XGBoost ML model for segment risk scoring
- **Route Optimization**: NetworkX-based routing with multiple strategies
- **Field Reporting**: Submit and track disruption reports

## Prerequisites

- Python 3.9+
- Docker & Docker Compose (for PostgreSQL + PostGIS + Redis)
- OpenWeatherMap API key (free tier)

## Setup

### 1. Start Infrastructure

```bash
cd backend
docker compose up -d
```

This starts:
- PostgreSQL 15 with PostGIS 3.3 on port 5432
- Redis 7 on port 6379

### 2. Python Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuration

```bash
cp .env.example .env
```

Edit `.env` and add your OpenWeatherMap API key:
```
OPENWEATHERMAP_API_KEY=your_key_here
```

Get a free key at: https://openweathermap.org/api

### 4. Initialize Database

```bash
# Set Python path (important!)
# Windows:
set PYTHONPATH=%cd%
# macOS/Linux:
export PYTHONPATH=$(pwd)

# Create tables
python -m app.scripts.init_db

# Load sample corridor (6 nodes)
python -m app.scripts.load_sample_roads

# Generate synthetic data (vehicles + disruption history)
python -m app.scripts.seed_synthetic_data
```

### 5. Train ML Model & Score Segments

```bash
# Train risk prediction model (~30 seconds)
python -m app.ml.train_risk_model

# Score all segments with current risk
python -m app.ml.score_segments
```

### 6. Start API Server

```bash
uvicorn app.main:app --reload
```

API available at:
- **Base**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## API Endpoints

### Roads
- `GET /roads` - List all road segments
- `GET /roads/{id}` - Get specific segment
- `GET /roads/nodes/` - List all nodes

### Vehicles
- `GET /vehicles` - List vehicles
- `GET /vehicles/{id}` - Get vehicle details
- `POST /vehicles/{id}/position` - Update GPS position
- `GET /vehicles/{id}/positions` - Get position history

### Weather
- `GET /weather/latest?hours=6` - Recent weather readings
- `POST /weather/ingest` - Ingest weather data

### Reports
- `GET /reports` - List field reports
- `POST /reports` - Submit new report
- `PATCH /reports/{id}` - Update report status

### Risk & Routing
- `GET /risk/scores` - Get risk scores for segments
- `GET /route?from_node_id=1&to_node_id=6&mode=balanced` - Calculate route
  - Modes: `balanced`, `safest`, `fastest`

## Advanced Usage

### Simulate GPS Updates

Run continuous vehicle movement simulation:

```bash
python -m app.scripts.simulate_gps
```

Press Ctrl+C to stop.

### Fetch Real OSM Data

Replace placeholder roads with real OpenStreetMap data:

```bash
python -m app.scripts.fetch_osm_roads
```

**Requirements**: Internet connection, 2-5 minutes

After loading OSM data, re-run:
```bash
python -m app.scripts.seed_synthetic_data
python -m app.ml.train_risk_model
python -m app.ml.score_segments
```

### Fetch Real Weather

Pull current weather from OpenWeatherMap:

```bash
python -m app.scripts.fetch_weather
```

Then update risk scores:
```bash
python -m app.ml.score_segments
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── database.py          # DB connection
│   ├── models/              # SQLAlchemy models
│   │   ├── road.py
│   │   ├── vehicle.py
│   │   ├── weather.py
│   │   ├── report.py
│   │   └── analytics.py
│   ├── schemas/             # Pydantic schemas
│   ├── api/                 # API routes
│   │   ├── roads.py
│   │   ├── vehicles.py
│   │   ├── weather.py
│   │   ├── reports.py
│   │   ├── risk.py
│   │   └── routing.py
│   ├── ml/                  # Machine learning
│   │   ├── features.py
│   │   ├── train_risk_model.py
│   │   └── score_segments.py
│   ├── routing/             # Route engine
│   │   ├── graph_builder.py
│   │   └── route_engine.py
│   └── scripts/             # Utility scripts
│       ├── init_db.py
│       ├── load_sample_roads.py
│       ├── seed_synthetic_data.py
│       ├── simulate_gps.py
│       ├── fetch_osm_roads.py
│       └── fetch_weather.py
├── models/                  # Trained ML models (created)
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Database Schema

**10 tables:**
- `road_nodes` - Junction/waypoint locations
- `road_segments` - Road segments between nodes
- `vehicles` - Tracked vehicles
- `vehicle_positions` - GPS history
- `weather_readings` - Weather observations
- `field_reports` - User-submitted disruption reports
- `disruption_history` - Historical events for ML training
- `risk_scores` - ML-predicted segment risk
- `accessibility_scores` - GIS accessibility metrics (planned)
- `alerts` - Real-time notifications (planned)

## ML Model Details

**Risk Prediction Model**: XGBoost binary classifier

**Features**:
- Temporal: Month, day of year, monsoon season flag
- Terrain: Flat/hilly/mountainous
- Weather: Precipitation, temperature, wind
- Historical: Recent disruptions (90-day window)

**Training**:
- 2 years synthetic disruption history
- Chronological train/test split (last 60 days held out)
- ~2% disruption rate (realistic for NER terrain)

**Metrics**:
- ROC-AUC: Primary metric (ranking quality)
- Correctly ranks hilly segments 5-8x riskier than flat

**Known Limitation**: Low threshold accuracy expected with rare events. Route engine uses raw probabilities for ranking, not binary classification.

## Testing

```bash
pytest
```

## Troubleshooting

### Database Connection Error

Check Docker containers:
```bash
docker compose ps
docker compose logs postgres
```

Restart if needed:
```bash
docker compose down
docker compose up -d
```

### PYTHONPATH Issues

Always set before running scripts:
```bash
# Windows
set PYTHONPATH=%cd%

# macOS/Linux
export PYTHONPATH=$(pwd)
```

### Import Errors

Ensure you're in the `backend/` directory and virtual environment is activated.

### Model Not Found

Run training first:
```bash
python -m app.ml.train_risk_model
```

## Development

### Adding New Features

1. Models: Add to `app/models/`
2. Schemas: Add to `app/schemas/`
3. Routes: Add to `app/api/`
4. Register router in `app/main.py`

### Database Migrations

For schema changes, consider adding Alembic:
```bash
alembic init alembic
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## License

MIT License

## Team

Smart India Hackathon 2026 - NER Logistics Team
