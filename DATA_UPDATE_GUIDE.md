# Data Update & Training Guide - NER Smart Logistics Platform

## Table of Contents
1. [Updating Road Network Data](#1-updating-road-network-data)
2. [Real-Time Data Sources for NER](#2-real-time-data-sources-for-ner)
3. [Weather Data Integration](#3-weather-data-integration)
4. [Disruption Data Collection](#4-disruption-data-collection)
5. [Retraining the ML Model](#5-retraining-the-ml-model)
6. [Complete Update Workflow](#6-complete-update-workflow)

---

## 1. Updating Road Network Data

### Option A: Load Real OSM Data (Recommended)

**This replaces the 6-node sample with real roads, intersections, and alternate routes.**

```bash
cd E:\Mark2\ner-logistics-platform\backend

# Activate environment
source venv/Scripts/activate   # Git Bash
# OR
venv\Scripts\activate          # CMD

# Set Python path
export PYTHONPATH=/e/Mark2/ner-logistics-platform/backend  # Git Bash
# OR
set PYTHONPATH=E:\Mark2\ner-logistics-platform\backend      # CMD

# Install osmnx if not already installed
pip install osmnx

# Fetch real OSM data (takes 2-5 minutes)
python -m app.scripts.fetch_osm_roads
```

**What this does:**
- Downloads real road network from OpenStreetMap
- Covers Guwahati-Shillong corridor (defined in `.env`)
- Includes actual intersections and alternate routes
- Replaces synthetic 6-node network with hundreds of real nodes

**Coverage area** (from `.env`):
```
CORRIDOR_MIN_LAT=25.5
CORRIDOR_MAX_LAT=26.2
CORRIDOR_MIN_LON=91.5
CORRIDOR_MAX_LON=92.0
```

**To expand to more NER regions**, edit `.env`:
```bash
# Example: Cover entire Meghalaya + parts of Assam
CORRIDOR_MIN_LAT=25.0    # Further south
CORRIDOR_MAX_LAT=26.5    # Further north
CORRIDOR_MIN_LON=90.5    # Further west
CORRIDOR_MAX_LON=92.5    # Further east
```

### Option B: Expand Sample Network Manually

Edit `app/scripts/load_sample_roads.py` to add more corridors:

```python
# Add more routes
nodes_data = [
    # Existing Guwahati-Shillong
    {"name": "Guwahati", "lat": 26.1445, "lon": 91.7362, "type": "town"},
    # ... existing nodes ...
    
    # NEW: Guwahati-Tezpur route
    {"name": "Tezpur", "lat": 26.6338, "lon": 92.7834, "type": "town"},
    {"name": "Nagaon", "lat": 26.3484, "lon": 92.6828, "type": "town"},
    
    # NEW: Shillong-Silchar route
    {"name": "Silchar", "lat": 24.8333, "lon": 92.7789, "type": "town"},
]
```

---

## 2. Real-Time Data Sources for NER

### A. Weather Data

#### **OpenWeatherMap** (Recommended - FREE)
- **URL**: https://openweathermap.org/api
- **Free Tier**: 1,000 calls/day
- **Coverage**: All NER cities

**Setup:**
1. Sign up at https://openweathermap.org/api
2. Get API key
3. Add to `.env`:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```
4. Run:
   ```bash
   python -m app.scripts.fetch_weather
   ```

**Key cities to monitor:**
- Guwahati (26.1445, 91.7362)
- Shillong (25.5788, 91.8933)
- Imphal (24.8170, 93.9368)
- Agartala (23.8315, 91.2868)
- Aizawl (23.7271, 92.7176)
- Itanagar (27.0844, 93.6053)
- Kohima (25.6747, 94.1081)

#### **India Meteorological Department (IMD)**
- **URL**: https://mausam.imd.gov.in/
- **Data**: Official weather warnings, monsoon forecasts
- **Format**: Manual reports (no easy API)
- **Use**: Cross-reference for monsoon risk periods

### B. Road Disruption Data

#### **1. National Disaster Management Authority (NDMA)**
- **URL**: https://ndma.gov.in/
- **Data**: Landslides, floods, earthquake damage
- **Format**: PDF reports, press releases
- **How to use**: Manual extraction → feed into `disruption_history` table

```bash
# Example: Add a disruption manually via API
curl -X POST http://localhost:8000/reports \
  -H "Content-Type: application/json" \
  -d '{
    "segment_id": 5,
    "report_type": "landslide",
    "severity": "high",
    "description": "Landslide blocking NH40 at Umsning",
    "latitude": 25.8655,
    "longitude": 91.7852,
    "reporter_name": "Field Officer",
    "reporter_contact": "+91-XXXXXXXXXX"
  }'
```

#### **2. Ministry of Road Transport & Highways**
- **URL**: https://morth.nic.in/
- **Data**: Highway status, construction updates
- **API**: None (manual scraping required)

#### **3. State PWD Departments**
- Assam PWD: https://pwd.assam.gov.in/
- Meghalaya PWD: https://megpwd.gov.in/
- Manipur PWD: https://manipur.gov.in/
- **Data**: Road closures, maintenance schedules
- **Access**: Manual checking or contact departments

#### **4. Social Media Monitoring** (Advanced)
- Twitter/X: Monitor #NERoads, #AssamFloods, #MeghalayaLandslide
- Local news: The Shillong Times, Assam Tribune
- **Tool**: Use Twitter API or web scraping

### C. Traffic & GPS Data

#### **Option 1: Google Roads API** (Paid)
- **URL**: https://developers.google.com/maps/documentation/roads
- **Data**: Real-time traffic, speed limits
- **Cost**: $0.005 per request

#### **Option 2: MapMyIndia (India-specific)**
- **URL**: https://www.mapmyindia.com/api/
- **Data**: Traffic, toll plazas, POIs
- **Coverage**: Better for Indian roads than Google

#### **Option 3: Simulate Your Own GPS** (Demo/Testing)
Already built in the project:
```bash
python -m app.scripts.simulate_gps
```

### D. Elevation Data (for Terrain Classification)

#### **SRTM Data** (Shuttle Radar Topography Mission)
- **URL**: https://srtm.csi.cgiar.org/
- **Coverage**: Global 90m resolution
- **Format**: GeoTIFF files

**How to use:**
1. Download SRTM tiles for NER
2. Use `rasterio` or `GDAL` to extract elevation
3. Classify terrain:
   - 0-200m elevation: `flat`
   - 200-1000m: `hilly`
   - >1000m: `mountainous`

**Quick integration:**
```python
import rasterio

def get_elevation(lat, lon, raster_path):
    with rasterio.open(raster_path) as dataset:
        # Convert lat/lon to row/col
        row, col = dataset.index(lon, lat)
        elevation = dataset.read(1)[row, col]
    return elevation

# Classify
def classify_terrain(elevation):
    if elevation < 200:
        return "flat"
    elif elevation < 1000:
        return "hilly"
    else:
        return "mountainous"
```

---

## 3. Weather Data Integration

### Step-by-Step Setup

**1. Get API Key**
- Sign up at https://openweathermap.org/api
- Copy your API key

**2. Update Configuration**
Edit `E:\Mark2\ner-logistics-platform\backend\.env`:
```bash
OPENWEATHERMAP_API_KEY=your_actual_key_here
```

**3. Test Weather Fetch**
```bash
cd E:\Mark2\ner-logistics-platform\backend
source venv/Scripts/activate
export PYTHONPATH=/e/Mark2/ner-logistics-platform/backend

python -m app.scripts.fetch_weather
```

**4. Set Up Automatic Updates**

**Option A: Windows Task Scheduler**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 6 AM
4. Action: Start a program
   - Program: `E:\Mark2\ner-logistics-platform\backend\venv\Scripts\python.exe`
   - Arguments: `-m app.scripts.fetch_weather`
   - Start in: `E:\Mark2\ner-logistics-platform\backend`

**Option B: Python Script with Loop**
Create `auto_weather_updater.py`:
```python
import schedule
import time
from app.scripts.fetch_weather import fetch_weather

def job():
    print("Fetching weather...")
    fetch_weather()

# Run every 6 hours
schedule.every(6).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Run:
```bash
python auto_weather_updater.py
```

---

## 4. Disruption Data Collection

### Method 1: Manual Entry via API

```bash
curl -X POST http://localhost:8000/reports \
  -H "Content-Type: application/json" \
  -d '{
    "segment_id": 3,
    "report_type": "landslide",
    "severity": "critical",
    "description": "Complete road blockage due to landslide",
    "latitude": 25.9015,
    "longitude": 91.8797,
    "reporter_name": "Highway Patrol",
    "reporter_contact": "+91-9876543210",
    "images": ["https://example.com/photo1.jpg"]
  }'
```

### Method 2: Web Scraping NDMA/News

Create `scrape_ndma.py`:
```python
import requests
from bs4 import BeautifulSoup
from app.database import SessionLocal
from app.models import DisruptionHistory
from datetime import datetime

def scrape_ndma_reports():
    """Scrape NDMA for NER disaster reports."""
    url = "https://ndma.gov.in/Disaster-Updates"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    db = SessionLocal()
    
    # Parse reports (adjust selectors based on actual site structure)
    for report in soup.find_all('div', class_='report'):
        title = report.find('h3').text
        date = report.find('span', class_='date').text
        
        # Check if it's NER-related
        if any(region in title for region in ['Meghalaya', 'Assam', 'Manipur']):
            # Extract details and save
            disruption = DisruptionHistory(
                segment_id=None,  # Manual mapping needed
                disruption_type='landslide',
                severity='high',
                started_at=datetime.strptime(date, '%Y-%m-%d'),
                description=title,
                is_synthetic=False
            )
            db.add(disruption)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    scrape_ndma_reports()
```

### Method 3: Mobile App Reporting (Phase 2)

Your Flutter app (to be built) should POST to:
```
POST /reports
```

With image upload support.

---

## 5. Retraining the ML Model

### When to Retrain

Retrain the model when:
1. **You load real OSM data** (new road segments)
2. **You add real disruption history** (better training data)
3. **Weather patterns change** (seasonal updates)
4. **Model performance degrades** (monitor accuracy)

### Full Retrain Workflow

```bash
cd E:\Mark2\ner-logistics-platform\backend
source venv/Scripts/activate
export PYTHONPATH=/e/Mark2/ner-logistics-platform/backend

# Step 1: Ensure you have enough disruption data
# (At least 50-100 real disruption events for good performance)

# Step 2: Retrain the model
python -m app.ml.train_risk_model

# Step 3: Score all segments with new model
python -m app.ml.score_segments

# Step 4: Verify improvement
# Check ROC-AUC in the training output
# Old: 0.693
# New: Should be higher with real data
```

### Understanding the Training Output

```
Building training dataset...
Dataset shape: (3660, 11)  ← Number of training samples
Disruption rate: 1.4%      ← Percentage of disruption events

ROC-AUC: 0.693            ← KEY METRIC (higher = better)
                             0.5 = random guessing
                             1.0 = perfect prediction
                             >0.7 = good

Feature Importance:
is_monsoon            0.439  ← Most important feature
recent_disruptions    0.255
month                 0.081
is_mountainous        0.066
```

### Improving Model Performance

**1. Add More Real Disruption Data**
- Current: 104 synthetic events
- Target: 500+ real events for production
- Focus on monsoon season (June-September)

**2. Add More Features**

Edit `app/ml/features.py` to add:
```python
def extract_features_for_training(segment_id, date, db):
    # ... existing features ...
    
    # NEW: Add elevation gain
    features['elevation_gain_m'] = calculate_elevation_gain(segment)
    
    # NEW: Add traffic volume
    features['avg_daily_traffic'] = get_traffic_volume(segment)
    
    # NEW: Add proximity to water bodies
    features['near_river'] = is_near_river(segment)
    
    # NEW: Add road condition score
    features['road_condition'] = get_road_condition(segment)
    
    return features
```

**3. Try Different Models**

Edit `app/ml/train_risk_model.py`:
```python
# Current: XGBoost
model = xgb.XGBClassifier(...)

# Try: Random Forest
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=200, max_depth=10)

# Try: LightGBM (faster than XGBoost)
import lightgbm as lgb
model = lgb.LGBMClassifier(n_estimators=100)
```

**4. Tune Hyperparameters**

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth': [3, 5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [50, 100, 200]
}

model = xgb.XGBClassifier()
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='roc_auc')
grid_search.fit(X_train, y_train)

print(f"Best params: {grid_search.best_params_}")
print(f"Best ROC-AUC: {grid_search.best_score_}")
```

---

## 6. Complete Update Workflow

### Scenario: Starting Fresh with Real Data

```bash
# 1. Load real OSM road network
cd E:\Mark2\ner-logistics-platform\backend
source venv/Scripts/activate
export PYTHONPATH=/e/Mark2/ner-logistics-platform/backend

python -m app.scripts.fetch_osm_roads
# Wait 2-5 minutes...

# 2. Set up weather API
# Edit .env and add your OpenWeatherMap key
python -m app.scripts.fetch_weather

# 3. Generate disruption data (still synthetic for now)
python -m app.scripts.seed_synthetic_data

# 4. Train ML model on new network
python -m app.ml.train_risk_model

# 5. Score all segments
python -m app.ml.score_segments

# 6. Restart API server
uvicorn app.main:app --reload

# 7. Test
curl "http://localhost:8000/route?from_node_id=1&to_node_id=100&mode=balanced"
```

### Scenario: Adding Real Disruption Events

```bash
# Option 1: Via API (one by one)
curl -X POST http://localhost:8000/reports -H "Content-Type: application/json" -d @disruption1.json
curl -X POST http://localhost:8000/reports -H "Content-Type: application/json" -d @disruption2.json

# Option 2: Bulk import from CSV
python import_disruptions.py historical_data.csv

# Then retrain
python -m app.ml.train_risk_model
python -m app.ml.score_segments
```

### Scenario: Expanding to New NER Region

```bash
# 1. Update .env with new bounding box
# Example: Add Manipur
CORRIDOR_MIN_LAT=24.0
CORRIDOR_MAX_LAT=25.5
CORRIDOR_MIN_LON=93.0
CORRIDOR_MAX_LON=94.5

# 2. Fetch OSM data
python -m app.scripts.fetch_osm_roads

# 3. Add disruption history for that region
# (Manual data entry or scraping)

# 4. Retrain model
python -m app.ml.train_risk_model
python -m app.ml.score_segments
```

---

## Quick Reference: Data Sources Summary

| Data Type | Source | Access | Update Frequency |
|-----------|--------|--------|------------------|
| **Roads** | OpenStreetMap | Free API | Monthly |
| **Weather** | OpenWeatherMap | Free (1k calls/day) | Hourly |
| **Disruptions** | NDMA Reports | Manual/Scraping | Weekly |
| **Elevation** | SRTM | Free Download | One-time |
| **Traffic** | Google/MapMyIndia | Paid API | Real-time |
| **News** | Local Media | Scraping | Daily |

---

## Troubleshooting

### OSM Fetch Fails
```
Error: Overpass API timeout
```
**Solution**: Reduce bounding box size or try again later.

### Weather API Errors
```
Error: 401 Unauthorized
```
**Solution**: Check API key in `.env` file.

### Model Training Crashes
```
MemoryError: Unable to allocate array
```
**Solution**: Reduce dataset size or use a machine with more RAM.

### Low Model Performance
```
ROC-AUC: 0.52 (not much better than random)
```
**Solution**: 
- Add more real disruption data
- Check feature quality (are they informative?)
- Try different model (Random Forest, LightGBM)

---

**Last Updated**: September 21, 2026  
**Next Review**: After Phase 2 (Real-time alerts & mobile app)
