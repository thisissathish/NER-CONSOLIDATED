# UrbanFlow AI - Backend

FastAPI backend for UrbanFlow AI, providing AI-powered intelligent routing, real-time vehicle tracking, and risk assessment for urban road networks.

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

# Load sample corridor (demo)
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
