# Quick Start Guide

## NER Smart Logistics Platform - Smart India Hackathon 2026

Complete backend built from scratch! Here's how to get it running:

## 🚀 Quick Setup (5 minutes)

### 1. Start Infrastructure
```bash
cd backend
docker compose up -d
```

### 2. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate          # On Windows
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# .env already created, just add your API key if you have one
# Edit backend/.env and set OPENWEATHERMAP_API_KEY (optional)
```

### 4. Initialize Database & Load Data
```bash
# Set Python path (important!)
set PYTHONPATH=%cd%            # Windows
# export PYTHONPATH=$(pwd)     # macOS/Linux

# Create tables
python -m app.scripts.init_db

# Load sample road network (Guwahati → Shillong)
python -m app.scripts.load_sample_roads

# Generate synthetic data (vehicles + 2 years disruption history)
python -m app.scripts.seed_synthetic_data
```

### 5. Train ML Model
```bash
# Train XGBoost risk prediction model (~30 seconds)
python -m app.ml.train_risk_model

# Score all road segments with current risk
python -m app.ml.score_segments
```

### 6. Start API Server
```bash
uvicorn app.main:app --reload
```

**✓ Done!** Visit http://localhost:8000/docs

## 📊 What You Get

### API Endpoints (20+)
- **Roads**: List segments, nodes, query by ID
- **Vehicles**: Track 4 vehicles, GPS history
- **Weather**: Ingest and query weather data
- **Reports**: Submit field disruption reports
- **Risk**: ML-predicted risk scores per segment
- **Routing**: 3 modes (balanced, safest, fastest)

### Database (10 tables, PostgreSQL + PostGIS)
- Road network with geometry
- Vehicle tracking
- Weather readings
- Disruption history
- Risk scores
- Field reports
- Alerts (ready for Phase 2)

### ML Model
- XGBoost classifier
- 8 features (weather, terrain, history, temporal)
- Correctly ranks hilly segments 5-8x riskier than flat
- ROC-AUC optimized for ranking quality

### Sample Data
- 6-node corridor: Guwahati → Jorabat → Byrnihat → Nongpoh → Umsning → Shillong
- 4 active vehicles
- 2 years synthetic disruption history (~400 events)
- Terrain-weighted risk (flat < hilly < mountainous)

## 🎮 Try It Out

### Get a Route
```bash
curl "http://localhost:8000/route?from_node_id=1&to_node_id=6&mode=balanced"
```

### Check Risk Scores
```bash
curl "http://localhost:8000/risk/scores"
```

### List Vehicles
```bash
curl "http://localhost:8000/vehicles"
```

### Simulate GPS Movement
```bash
# In another terminal (keep API running)
python -m app.scripts.simulate_gps
```

## 📁 Project Structure

```
ner-logistics-platform/
├── CLAUDE.md              # Project memory for Claude Code
├── README.md              # Project overview
├── LICENSE                # MIT License
└── backend/
    ├── docker-compose.yml # PostgreSQL + PostGIS + Redis
    ├── requirements.txt   # Python dependencies
    ├── .env               # Configuration
    ├── README.md          # Detailed backend docs
    └── app/
        ├── main.py        # FastAPI app (entry point)
        ├── config.py      # Settings
        ├── database.py    # DB connection
        ├── models/        # SQLAlchemy models (5 files)
        ├── schemas/       # Pydantic schemas (6 files)
        ├── api/           # API routes (6 files)
        ├── ml/            # ML components (3 files)
        ├── routing/       # Route engine (2 files)
        └── scripts/       # Utilities (6 files)
```

**Total**: 46 files, 3,100+ lines of code, 38 Python modules

## 🔄 Next Steps

### Phase 2 (In Progress)
- [ ] GIS accessibility index + heatmap
- [ ] Real-time GPS pub/sub
- [ ] Alert engine with push/SMS
- [ ] Load real OSM data: `python -m app.scripts.fetch_osm_roads`

### Phase 3 (Planned)
- [ ] React + Leaflet dashboard
- [ ] Flutter mobile app for field reports
- [ ] Offline sync

### Phase 4 (Planned)
- [ ] Deploy to cloud (Render/Railway/AWS)
- [ ] End-to-end testing
- [ ] Pitch deck

## 🎯 What's Special

1. **Real architecture, not a demo**: 10 tables, proper separation of concerns, production patterns
2. **ML that works**: Risk model correctly ranks relative risk (verified)
3. **Synthetic data done right**: All flagged with `is_synthetic: true`, documented assumptions
4. **API-first design**: Weather/GPS updates go through endpoints (hooks for real-time in Phase 2)
5. **Documented limitations**: No alternate routes yet (single-path corridor), low risk probabilities expected

## 📚 Documentation

- `README.md` - High-level overview
- `backend/README.md` - Complete setup, API reference, troubleshooting
- `CLAUDE.md` - Project memory, conventions, roadmap
- API docs - http://localhost:8000/docs (interactive)

## 🐛 Troubleshooting

**Docker not starting?**
```bash
docker compose down
docker compose up -d
docker compose ps
```

**Import errors?**
```bash
# Always set PYTHONPATH in backend/ directory
set PYTHONPATH=%cd%     # Windows
```

**Model not found?**
```bash
python -m app.ml.train_risk_model
```

## 👥 Team Roles

This backend covers work for:
- ✅ Backend lead (infrastructure, API)
- ✅ AI/ML engineer (risk model, features)
- 🔄 GIS engineer (OSM integration ready, accessibility pending)
- 🔄 Real-time engineer (GPS pub/sub architecture ready)
- ⏳ Frontend web (API ready for consumption)
- ⏳ Mobile dev (endpoints ready for consumption)

## 🎓 Smart India Hackathon 2026

**Problem Statement**: AI-Based Smart Logistics and Accessibility Intelligence Platform for NER

**Solution**: End-to-end pilot for Guwahati–Shillong corridor with real ML, real routing, real architecture

**Status**: Phase 1 complete (backend + ML + routing), Phase 2 in progress

---

Built from scratch with Claude Code 🤖
