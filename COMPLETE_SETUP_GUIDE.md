# UrbanFlow AI - Complete Setup Guide

**Last Updated**: September 30, 2026  
**Version**: 2.0 (Phase 2 Complete)

---

## 📋 Prerequisites

### Required
- Windows 10/11
- Python 3.10+
- Git
- 8GB RAM minimum

### Optional (Recommended)
- Docker Desktop (for PostgreSQL + Redis)
- Node.js 18+ (for React frontend)
- OpenWeatherMap API key (free tier)
- Twilio account (for SMS alerts)
- Firebase project (for push notifications)

---

## 🚀 Quick Start (5 Minutes)

### Option A: With Docker (Recommended)

```powershell
# 1. Navigate to project
cd E:\Mark2\NER-CONSOLIDATED\backend

# 2. Start Docker containers
docker compose up -d

# 3. Activate Python virtual environment
.\venv\Scripts\activate

# 4. Install dependencies (if not already done)
pip install -r requirements.txt

# 5. Initialize database
$env:PYTHONPATH = "E:\Mark2\NER-CONSOLIDATED\backend"
python -m app.scripts.init_db
python -m app.scripts.load_sample_roads
python -m app.scripts.seed_synthetic_data

# 6. Train ML model
python -m app.ml.train_risk_model
python -m app.ml.score_segments

# 7. Start API server
uvicorn app.main:app --reload --port 8000
```

### Option B: Without Docker (Manual PostgreSQL Setup)

If you don't have Docker, install PostgreSQL 15+ and Redis manually, then update `.env` with your connection strings.

---

## 🎨 Start the React Dashboard

```powershell
# In a new terminal
cd E:\Mark2\NER-CONSOLIDATED\frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Access at: **http://localhost:3000**

---

## 🔧 Configuration

### 1. Environment Variables

Edit `backend/.env` (use `backend/.env.example` as a template):

```env
# Database (required)
DATABASE_URL=postgresql://urbanflow_user:urbanflow_pass@localhost:5432/urbanflow

# Redis (required for caching)
REDIS_URL=redis://localhost:6379/0

# OpenWeatherMap (optional - for live weather)
OPENWEATHERMAP_API_KEY=your_key_here

# Application
DEBUG=True
APP_NAME=UrbanFlow AI
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────┐
│           React Frontend (Port 3000)            │
│  • Dashboard • Vehicles • Alerts • Routing      │
└────────────────┬────────────────────────────────┘
                 │ HTTP REST / WebSocket
┌────────────────▼────────────────────────────────┐
│         FastAPI Backend (Port 8000)             │
│  • 30+ REST endpoints                           │
│  • WebSocket for real-time updates              │
│  • Alert engine                                 │
│  • ML risk scoring                              │
│  • Route optimization                           │
└──┬────────┬───────────┬──────────────────┬──────┘
   │        │           │                  │
   ▼        ▼           ▼                  ▼
┌──────┐ ┌──────┐ ┌──────────┐ ┌────────────────┐
│ Post │ │Redis │ │ XGBoost  │ │  Notification  │
│ greSQL│ │Cache │ │   Model  │ │   Services     │
│+PostGIS│ │     │ │          │ │ (Twilio/       │
│      │ │      │ │          │ │  Firebase)     │
└──────┘ └──────┘ └──────────┘ └────────────────┘
```
