# Phase 2 Implementation Plan - Missing Features
**Project**: NER Smart Logistics Platform  
**Date**: September 21, 2026  
**Status**: Ready to implement missing features

---

## 🎯 Missing Features Overview

### Priority 1: Data Integration (Foundational)
1. ✅ Real OpenStreetMap data (script ready)
2. ✅ Live weather integration (script ready)
3. ⏳ SRTM elevation data for accurate terrain classification

### Priority 2: Core Features
4. ⏳ GIS Accessibility Index
5. ⏳ Real-time GPS tracking with WebSocket
6. ⏳ Alert engine with push/SMS notifications

### Priority 3: Frontend Applications
7. ⏳ React + Leaflet web dashboard
8. ⏳ Flutter mobile app for field reporting

### Priority 4: Production Deployment
9. ⏳ Cloud deployment (AWS/Render/Railway)
10. ⏳ CI/CD pipeline
11. ⏳ Monitoring and logging

---

## 📋 Implementation Roadmap

### Week 1: Data Integration (Days 1-3)

#### Day 1: Real OpenStreetMap Integration
**Status**: Script ready, needs execution  
**Time**: 2-3 hours

**Tasks:**
- [ ] Create `.env` file with configuration
- [ ] Install `osmnx` package
- [ ] Run `fetch_osm_roads.py` to download real road network
- [ ] Verify node/segment counts (expect 500+ nodes vs current 6)
- [ ] Re-train ML model on expanded network
- [ ] Test route optimization with alternate paths

**Commands:**
```bash
cd D:\Predictx\NER-smart-logistics-master\backend

# Create .env from template
copy .env.example .env

# Install osmnx
pip install osmnx

# Fetch OSM data (takes 2-5 minutes)
python -m app.scripts.fetch_osm_roads

# Re-seed disruption history
python -m app.scripts.seed_synthetic_data

# Retrain model
python -m app.ml.train_risk_model

# Re-score segments
python -m app.ml.score_segments
```

**Expected Results:**
- Real intersection graph with alternate routes
- Route optimization modes now return different paths
- Improved ML model with more training data

---

#### Day 2: Live Weather Integration
**Status**: Script ready, needs API key  
**Time**: 1-2 hours

**Tasks:**
- [ ] Sign up for OpenWeatherMap API (free tier: 1,000 calls/day)
- [ ] Add `OPENWEATHERMAP_API_KEY` to `.env`
- [ ] Run `fetch_weather.py` manually
- [ ] Set up Windows Task Scheduler for hourly updates
- [ ] Verify weather data in database
- [ ] Test ML scoring with real weather

**Commands:**
```bash
# Add to .env:
# OPENWEATHERMAP_API_KEY=your_key_here

# Fetch weather once
python -m app.scripts.fetch_weather

# Re-score with real weather
python -m app.ml.score_segments
```

**Automation (Windows Task Scheduler):**
```powershell
# Create scheduled task for hourly weather updates
$action = New-ScheduledTaskAction -Execute "python" -Argument "-m app.scripts.fetch_weather" -WorkingDirectory "D:\Predictx\NER-smart-logistics-master\backend"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName "NER-Weather-Update" -Action $action -Trigger $trigger
```

---

#### Day 3: Elevation Data for Terrain Classification
**Status**: Not implemented, needs new script  
**Time**: 3-4 hours

**Tasks:**
- [ ] Download SRTM elevation tiles for NER region
- [ ] Create `fetch_elevation.py` script
- [ ] Update `RoadSegment.terrain` based on elevation gain
- [ ] Retrain ML model with accurate terrain

**Implementation:**

Create `backend/app/scripts/fetch_elevation.py`:
```python
"""Fetch SRTM elevation data and classify terrain."""
import requests
from pathlib import Path

def fetch_srtm_tile(lat, lon):
    """Download SRTM 90m tile for given coordinates."""
    # SRTM tile naming: N25E091.hgt for latitude 25°N, longitude 91°E
    lat_str = f"{'N' if lat >= 0 else 'S'}{abs(int(lat)):02d}"
    lon_str = f"{'E' if lon >= 0 else 'W'}{abs(int(lon)):03d}"
    filename = f"{lat_str}{lon_str}.hgt"
    
    # Download from CGIAR SRTM (free, no signup)
    url = f"http://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/{filename}.zip"
    
    # TODO: Implement download, unzip, and parse
    pass

def classify_terrain_from_elevation(segment):
    """Classify segment terrain based on elevation profile."""
    # Get elevation at start and end
    # Calculate elevation gain per km
    # flat: < 50m gain per km
    # hilly: 50-200m gain per km
    # mountainous: > 200m gain per km
    pass
```

---

### Week 2: Core Backend Features (Days 4-7)

#### Day 4: GIS Accessibility Index
**Status**: Table exists, logic not implemented  
**Time**: 4-5 hours

**Tasks:**
- [ ] Create `calculate_accessibility.py` script
- [ ] Compute connectivity score (number of alternate routes)
- [ ] Calculate distance to nearest hospital/police station
- [ ] Measure mobile network coverage (using external API)
- [ ] Populate `accessibility_scores` table

**Metrics to Calculate:**
1. **Connectivity Score**: Number of alternate routes between major nodes
2. **Emergency Access**: Distance to hospitals, police stations
3. **Infrastructure Density**: Gas stations, repair shops within 20km
4. **Mobile Coverage**: Using OpenCelliD or similar API

---

#### Day 5-6: Real-Time GPS Tracking with WebSocket
**Status**: HTTP polling exists, needs WebSocket upgrade  
**Time**: 8-10 hours

**Tasks:**
- [ ] Install `fastapi[websockets]` package
- [ ] Create WebSocket endpoint `/ws/tracking`
- [ ] Implement pub/sub pattern with Redis
- [ ] Update `simulate_gps.py` to broadcast via WebSocket
- [ ] Update dashboard to connect to WebSocket
- [ ] Test real-time position updates

**Implementation Files:**
- `backend/app/api/websocket.py` - WebSocket routes
- `backend/app/services/pubsub.py` - Redis pub/sub handler
- `dashboard.html` - Add WebSocket client

---

#### Day 7: Alert Engine with Notifications
**Status**: Table exists, no trigger logic  
**Time**: 6-8 hours

**Tasks:**
- [ ] Create alert generation logic (risk threshold triggers)
- [ ] Implement push notification via Firebase
- [ ] Implement SMS via Twilio/MSG91
- [ ] Create alert management API endpoints
- [ ] Test notification delivery

**Alert Triggers:**
1. Segment risk > 10% (critical)
2. Weather warning (heavy rain, fog)
3. Field report filed on active route
4. Vehicle entering high-risk zone

---

### Week 3: Frontend Development (Days 8-14)

#### Day 8-10: React Dashboard
**Status**: Static HTML exists, needs React app  
**Time**: 12-15 hours

**Tech Stack:**
- React 18 with TypeScript
- Vite for build tooling
- React Leaflet for maps
- TanStack Query for data fetching
- Tailwind CSS for styling
- WebSocket for real-time updates

**Features:**
- Interactive risk heatmap
- Route planner with 3 mode toggles
- Real-time vehicle tracking
- Alert notifications panel
- Analytics dashboard (charts with Recharts)

---

#### Day 11-14: Flutter Mobile App
**Status**: Not started  
**Time**: 16-20 hours

**Features:**
- Field report submission with camera
- Offline map caching
- GPS tracking for field officers
- Push notification reception
- Route navigation integration

**Screens:**
1. Login/Auth
2. Map view with incident markers
3. Report submission form
4. Vehicle tracking list
5. Alert history

---

### Week 4: Production Deployment (Days 15-21)

#### Day 15-16: Dockerization
- [ ] Create production `Dockerfile` for FastAPI
- [ ] Multi-stage build for optimization
- [ ] Docker Compose for full stack
- [ ] Environment variable management

#### Day 17-18: Cloud Deployment
**Options:**
1. **Render** (Easiest): Free PostgreSQL, easy Docker deployment
2. **Railway**: Auto-scaling, GitHub integration
3. **AWS**: EC2 + RDS + S3, most scalable

**Tasks:**
- [ ] Set up cloud database (PostgreSQL + PostGIS)
- [ ] Deploy backend API
- [ ] Deploy frontend (Vercel/Netlify)
- [ ] Configure custom domain
- [ ] Set up SSL certificates

#### Day 19-20: CI/CD Pipeline
- [ ] GitHub Actions for testing
- [ ] Automated deployment on push to main
- [ ] Database migration strategy
- [ ] Rollback procedures

#### Day 21: Monitoring & Documentation
- [ ] Set up logging (Sentry or LogTail)
- [ ] Performance monitoring (Prometheus + Grafana)
- [ ] API documentation updates
- [ ] User guide and admin manual

---

## 🚀 Quick Start: First 3 Days

### Today (Day 1): Real OSM Data

**Goal**: Replace 6-node demo with real 500+ node network

```bash
cd D:\Predictx\NER-smart-logistics-master\backend

# 1. Create .env
echo DATABASE_URL=postgresql://ner_user:ner_pass@localhost:5432/ner_logistics > .env
echo OPENWEATHERMAP_API_KEY= >> .env
echo CORRIDOR_MIN_LAT=25.5 >> .env
echo CORRIDOR_MAX_LAT=26.2 >> .env
echo CORRIDOR_MIN_LON=91.5 >> .env
echo CORRIDOR_MAX_LON=92.0 >> .env

# 2. Install osmnx
pip install osmnx

# 3. Make sure Docker is running
docker compose up -d

# 4. Fetch OSM data (2-5 minutes)
python -m app.scripts.fetch_osm_roads

# 5. Re-seed and retrain
python -m app.scripts.seed_synthetic_data
python -m app.ml.train_risk_model
python -m app.ml.score_segments

# 6. Restart API
uvicorn app.main:app --reload

# 7. Test new routes
curl "http://localhost:8000/roads" | python -m json.tool | head -50
```

---

## 📊 Success Metrics

### Phase 2 Complete When:
- [ ] Real OSM road network loaded (500+ nodes)
- [ ] Live weather updates every hour
- [ ] Accessibility scores calculated
- [ ] WebSocket real-time tracking working
- [ ] Alert notifications delivered (push + SMS)
- [ ] React dashboard deployed
- [ ] Flutter app built and tested

### Phase 3 Complete When:
- [ ] Deployed to cloud with custom domain
- [ ] CI/CD pipeline operational
- [ ] Monitoring and logging active
- [ ] Load tested (100+ concurrent users)
- [ ] Documentation complete

---

## 🎯 Next Steps

**Right now, you should:**
1. Create the `.env` file
2. Run `fetch_osm_roads.py` to get real data
3. See the system work with actual alternate routes

**Want me to help with:**
- [ ] Creating the .env file?
- [ ] Running the OSM data fetch?
- [ ] Building the WebSocket real-time tracking?
- [ ] Creating the React dashboard?
- [ ] Building the Flutter mobile app?
- [ ] Deploying to cloud?

**Choose what to implement first, and I'll guide you step-by-step!**
