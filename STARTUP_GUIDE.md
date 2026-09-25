# NER Smart Logistics Platform - Manual Startup Guide

## Step-by-Step Startup

### 1. Start Docker Desktop
- Open Docker Desktop from Windows Start Menu
- Wait until the Docker icon in system tray shows "Docker Desktop is running"

### 2. Start Docker Containers
```cmd
cd backend
docker compose up -d
```

Wait 10-15 seconds for PostgreSQL and Redis to initialize.

### 3. Start API Server
```cmd
cd backend
venv\Scripts\activate
set PYTHONPATH=%cd%
uvicorn app.main:app --reload
```

### 4. Verify System is Running

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Dashboard: Open `dashboard.html` in your browser

---

## System URLs

| Resource | URL |
|----------|-----|
| API Docs (Swagger) | http://localhost:8000/docs |
| API Health Check | http://localhost:8000/health |
| Risk Scores | http://localhost:8000/risk/scores |
| Get Route | http://localhost:8000/route?from_node_id=7&to_node_id=12&mode=balanced |
| Dashboard | Open `dashboard.html` in browser |
| Route Comparison | Open `route_comparison.html` in browser |

---

## Common Tasks

### Check if Database is Ready
```cmd
cd backend
docker compose ps
```

### View API Logs
```cmd
# The API server window shows live logs
# Or check Docker logs:
docker compose logs postgres
docker compose logs redis
```

### Stop Everything
```cmd
cd backend
docker compose down
# Then press Ctrl+C in the API server window
```

### Restart After Stopping
```cmd
cd backend
docker compose up -d
# Wait 10 seconds
venv\Scripts\activate
set PYTHONPATH=%cd%
uvicorn app.main:app --reload
```

---

## If This is First Time Setup

If you haven't initialized the database yet, run these commands:

```cmd
cd backend
venv\Scripts\activate
set PYTHONPATH=%cd%

# Initialize database schema
python -m app.scripts.init_db

# Load sample road network
python -m app.scripts.load_sample_roads

# Generate synthetic data
python -m app.scripts.seed_synthetic_data

# Train ML model
python -m app.ml.train_risk_model

# Score road segments
python -m app.ml.score_segments
```

---

## Troubleshooting

### Docker containers won't start
**Error:** "Cannot connect to Docker daemon"
**Solution:** Make sure Docker Desktop is running

### Import errors when starting API
**Error:** "ModuleNotFoundError"
**Solution:** Make sure PYTHONPATH is set:
```cmd
set PYTHONPATH=%cd%
```

### API returns empty data
**Error:** Endpoints return `[]` or empty results
**Solution:** Database might be empty. Run the initialization scripts above.

### Port already in use
**Error:** "Address already in use"
**Solution:** 
```cmd
# Find what's using port 8000
netstat -ano | findstr :8000
# Kill that process or use a different port:
uvicorn app.main:app --reload --port 8001
```

---

## Next Steps After System is Running

1. **Test the API** - Visit http://localhost:8000/docs and try the endpoints
2. **View Dashboard** - Open `dashboard.html` in Chrome/Firefox
3. **Review Documentation** - Read `README.md` and `QUICKSTART.md`
4. **Check Demo Script** - See `DEMO_SCRIPT.txt` for presentation guidance
5. **Explore the Code** - Backend code is in `backend/app/`

---

## Post-Demo Development Tasks

Based on the project files, here are suggested next steps:

### Phase 2 Features
- [ ] Load real OSM data: `python -m app.scripts.fetch_osm_roads`
- [ ] Integrate weather API (add key to `.env`)
- [ ] Implement Alert engine & Notifications service
- [ ] Implement GIS accessibility scoring service
- [ ] Implement WebSocket real-time tracking
- [ ] Build React frontend dashboard
- [ ] Develop Flutter mobile app

### Documentation to Review
- `2_DAY_DEADLINE_PLAN.md` - Development roadmap
- `DATA_UPDATE_GUIDE.md` - How to update data and retrain ML model
- `DAY1_COMPLETE.md` - What's been completed
- `SETUP_COMPLETE.md` - System status and next steps

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `README.md` in the project root
3. Check `backend/README.md` for detailed API documentation
4. Review error logs in the terminal windows
