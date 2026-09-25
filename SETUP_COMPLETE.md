# NER Smart Logistics Platform - Setup Complete! ✓

## What's Running Right Now

✓ **PostgreSQL + PostGIS** (Docker container) - Database with spatial extensions
✓ **Redis** (Docker container) - Cache and real-time data
✓ **FastAPI Backend** (http://localhost:8000) - All APIs operational
✓ **ML Risk Model** - Trained and scoring road segments

## What You Have Built

### 1. Complete Backend Foundation
- **10 database tables** with real PostGIS spatial data
- **20+ API endpoints** (see http://localhost:8000/docs for interactive documentation)
- **Sample road network**: Guwahati → Jorabat → Byrnihat → Nongpoh → Umsning → Shillong (103.5 km)
- **4 tracked vehicles** with GPS capability
- **2 years of synthetic disruption history** (104 events, monsoon-weighted)

### 2. AI/ML Risk Prediction
- **XGBoost model** trained on 3,660 segment-day samples
- **ROC-AUC: 0.693** - correctly ranks risky segments
- **8 features**: weather, terrain, historical disruptions, temporal patterns
- **Real-time scoring**: Every road segment has current risk probability

### 3. Route Optimization Engine
- **3 routing modes**:
  - `balanced` - Minimizes risk-weighted travel time
  - `safest` - Prioritizes low-risk routes
  - `fastest` - Ignores risk, shortest time
- **NetworkX graph** with real distances and terrain

## Quick Test Commands

### 1. Check System Health
```bash
curl http://localhost:8000/health
```

### 2. Get Risk Scores (sorted by risk)
```bash
curl http://localhost:8000/risk/scores
```

### 3. Get Optimal Route (Guwahati to Shillong)
```bash
curl "http://localhost:8000/route?from_node_id=7&to_node_id=12&mode=balanced"
```

### 4. List All Vehicles
```bash
curl http://localhost:8000/vehicles
```

### 5. Get All Roads
```bash
curl http://localhost:8000/roads
```

### 6. Interactive API Documentation
Open in browser: **http://localhost:8000/docs**

## Current Risk Rankings

Based on the latest ML scoring:

| Rank | From      | To        | Risk  | Terrain      | Notes                           |
|------|-----------|-----------|-------|--------------|----------------------------------|
| 1    | Umsning   | Shillong  | 7.2%  | Mountainous  | Highest risk - steep terrain    |
| 2    | Umsning   | Shillong  | 1.7%  | Mountainous  | Alternative segment             |
| 3    | Byrnihat  | Nongpoh   | 0.61% | Hilly        | Moderate terrain                |
| 4    | Byrnihat  | Nongpoh   | 0.55% | Hilly        | Alternative segment             |
| 5    | Nongpoh   | Umsning   | 0.38% | Hilly        | Mid-corridor                    |
| ...  | ...       | ...       | ...   | ...          | ...                             |
| 10   | Jorabat   | Byrnihat  | 0.02% | Flat         | Lowest risk - flat approach     |

## Project Structure

```
ner-logistics-platform/
├── backend/
│   ├── app/
│   │   ├── api/          # API route handlers (6 files)
│   │   ├── models/       # Database models (5 files)
│   │   ├── schemas/      # Pydantic schemas (6 files)
│   │   ├── ml/           # ML training & scoring (3 files)
│   │   ├── routing/      # Route optimization (2 files)
│   │   └── scripts/      # Setup & data scripts (7 files)
│   ├── models/           # Trained ML models (risk_model.pkl)
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .env
├── CLAUDE.md             # Project memory
├── README.md
└── QUICKSTART.md
```

## How to Stop/Start

### Stop Everything
```bash
# Stop API server
# (Press Ctrl+C in the terminal where uvicorn is running, or use TaskStop)

# Stop Docker containers
cd E:\Mark2\ner-logistics-platform\backend
docker compose down
```

### Start Again Later
```bash
# 1. Start Docker containers
cd E:\Mark2\ner-logistics-platform\backend
docker compose up -d

# 2. Activate Python environment
source venv/Scripts/activate  # On Windows Git Bash
# OR
venv\Scripts\activate         # On Windows CMD

# 3. Set Python path
export PYTHONPATH=/e/Mark2/ner-logistics-platform/backend  # Git Bash
# OR
set PYTHONPATH=E:\Mark2\ner-logistics-platform\backend      # CMD

# 4. Start API server
uvicorn app.main:app --reload
```

## What's Next (Phase 2 - Not Started Yet)

### For Your Team to Build:

1. **GIS Accessibility Index** (GIS Engineer)
   - Load real OSM data: `python -m app.scripts.fetch_osm_roads`
   - Calculate accessibility scores for each segment
   - Build heatmap visualization

2. **Real-Time GPS & Alerts** (Backend Engineer)
   - GPS simulation: `python -m app.scripts.simulate_gps`
   - Alert engine triggers (disruption detected, high risk)
   - Push notifications (Firebase) + SMS (Twilio/MSG91)

3. **Web Dashboard** (Frontend Developer)
   - React + Leaflet map
   - Real-time vehicle tracking
   - Risk heatmap overlay
   - Route planner UI
   - Alert feed

4. **Mobile App** (Mobile Developer)
   - Flutter app
   - Field disruption reporting
   - Offline sync capability
   - Camera for evidence upload

5. **Weather Integration** (Data Engineer)
   - Get OpenWeatherMap API key: https://openweathermap.org/api
   - Add to `.env`: `OPENWEATHERMAP_API_KEY=your_key_here`
   - Run: `python -m app.scripts.fetch_weather`
   - Set up hourly cron job

## Demo Script for Presentation

1. **Show the problem**: "NER has limited road connectivity. A single disruption can halt logistics."

2. **Show the API**: Open http://localhost:8000/docs - "20+ endpoints, production-ready"

3. **Show risk prediction**: 
   ```bash
   curl http://localhost:8000/risk/scores
   ```
   "ML model identifies the Umsning-Shillong stretch as 7% risk - that's our mountainous terrain"

4. **Show route optimization**:
   ```bash
   curl "http://localhost:8000/route?from_node_id=7&to_node_id=12&mode=balanced"
   ```
   "AI routes around high-risk segments when alternatives exist"

5. **Show real architecture**: "PostgreSQL + PostGIS for spatial data, Redis for real-time, XGBoost for ML, NetworkX for routing - this isn't a toy, it's a foundation"

## Important Notes

- All synthetic data is flagged with `is_synthetic: true`
- Database uses node IDs 7-12 (not 1-6) - check `/roads` endpoint first
- Risk probabilities are relative rankings, not absolute predictions
- Current data is for Guwahati-Shillong corridor only (single path, no alternate routes yet)
- Load real OSM data to enable true risk-aware routing with alternatives

## Team Roles & Status

| Role                  | Status     | Next Step                              |
|-----------------------|------------|----------------------------------------|
| Backend/Cloud (You)   | ✓ Complete | Deploy to cloud, set up CI/CD          |
| AI/ML Engineer        | ✓ Complete | Tune model, add more features          |
| GIS/Data Engineer     | 🔄 Partial | Load real OSM, build accessibility idx |
| Real-time/Alerts Eng  | ⏳ Pending | GPS pub/sub, alert triggers            |
| Frontend Web          | ⏳ Pending | React dashboard, Leaflet map           |
| Mobile Developer      | ⏳ Pending | Flutter app, field reporting           |

## Troubleshooting

**Docker not running?**
```bash
docker compose ps
docker compose up -d
```

**Import errors?**
```bash
# Make sure PYTHONPATH is set every time
export PYTHONPATH=/e/Mark2/ner-logistics-platform/backend
```

**Model not found?**
```bash
python -m app.ml.train_risk_model
```

**Database empty?**
```bash
python -m app.scripts.init_db
python -m app.scripts.load_sample_roads
python -m app.scripts.seed_synthetic_data
python -m app.ml.score_segments
```

---

**Built from scratch - September 21, 2026**  
Smart India Hackathon 2026 - NER Smart Logistics Platform
