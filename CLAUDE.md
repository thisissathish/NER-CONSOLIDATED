# CLAUDE.md — NER Smart Logistics Platform (Smart India Hackathon)

This file is project memory for Claude Code. Drop it at the root of the
repo (next to `backend/`) and Claude Code will load it automatically at
the start of every session in this project.

## What this is

Smart India Hackathon prototype: "AI-Based Smart Logistics and
Accessibility Intelligence Platform for North Eastern Region (NER)."
6-person team. Expected solution per the problem statement: AI route
prediction/optimization, GIS accessibility dashboard, GPS vehicle
tracking, real-time alerts, mobile/web field reporting, weather/transport/
government API integration, cloud infra with offline support.

## Scope decision (locked in, don't relitigate without reason)

Building one pilot corridor end to end for real rather than a shallow
pass at the whole NER. **Pilot corridor: Guwahati–Shillong (NH40 / GS
Road).** Real data where free and fast to get (roads via OSM, weather via
OpenWeatherMap); synthetic data, clearly flagged as such, everywhere a
real feed would take too long to arrange (vehicle GPS, disruption
history, government/transport DB).

| Data layer | Status | Source |
|---|---|---|
| Roads | Placeholder (6 hand-placed waypoints) | Real: OSM via Overpass/osmnx, `fetch_osm_roads.py` |
| Weather | Integration built, untested with a real key | OpenWeatherMap free tier |
| Vehicle GPS | Synthetic, simulated along the road graph | No real source available in hackathon time |
| Disruption history | Synthetic, monsoon + terrain weighted | GSI/NDMA reports used only to shape the assumption, not as literal data |
| Govt/transport DB | Mocked endpoint | Presented as a planned integration point |

## Team and roles

1. Team lead — backend/cloud architecture, cross-team integration, pitch deck
2. AI/ML engineer — route optimization, risk model *(built — see below)*
3. GIS/data engineer — OSM ingestion, accessibility index *(not started)*
4. Backend — real-time/alerts — GPS ingestion, alert engine *(not started)*
5. Frontend web — dashboard *(not started)*
6. Mobile — field-reporting app *(not started)*

## Tech stack

FastAPI (Python) · PostgreSQL + PostGIS · Redis · SQLAlchemy + GeoAlchemy2
· networkx (routing) · XGBoost/scikit-learn (risk model) · osmnx (OSM
ingestion) · planned: React + Leaflet/Mapbox (web), Flutter (mobile),
Firebase (push) + Twilio/MSG91 (SMS), Docker (deploy).

## Build status

### Done — Backend foundation (`backend/`)

Real, running, tested end to end against a live PostGIS database (not
just written — actually executed, including finding and fixing one bug:
a missing `Vehicle.current_segment` relationship).

- 10 tables: `road_nodes`, `road_segments`, `vehicles`, `vehicle_positions`,
  `weather_readings`, `disruption_history`, `field_reports`, `risk_scores`,
  `accessibility_scores`, `alerts`. The last three are pre-created empty so
  the ML and GIS engineers don't wait on a migration.
- Endpoints: `/health`, `/roads`, `/roads/{id}`, `/nodes`, `/vehicles`,
  `POST /vehicles/{id}/position`, `/weather/latest`, `POST /weather/ingest`,
  `/reports` (GET/POST).
- Scripts: `init_db.py` (create tables), `load_sample_roads.py` (placeholder
  corridor), `seed_synthetic_data.py` (vehicles + disruption history),
  `simulate_gps.py` (moves vehicles, hits the live API), `fetch_osm_roads.py`
  (real OSM pull — needs real internet, won't run in a locked-down sandbox),
  `fetch_weather.py` (real OpenWeatherMap pull — needs an API key + real
  internet).

### Done — Route engine + ML risk model (`backend/app/ml/`, `backend/app/routing/`)

- `app/ml/features.py` — builds a synthetic per-segment-per-day training
  table (documents the modelling assumptions in the docstring — read it
  before changing the risk logic).
- `app/ml/train_risk_model.py` — XGBoost classifier, chronological
  train/test split. Tried `scale_pos_weight` to fix class imbalance first;
  it made the ranking worse on this small a sample, so it was reverted in
  favor of generating more synthetic training volume instead. That
  reasoning is in the code comments — don't re-add `scale_pos_weight`
  without re-checking that history.
- `app/ml/score_segments.py` — scores every segment, prefers a live
  weather reading within 6h if one exists, falls back to seasonal estimate.
- `app/routing/graph_builder.py` + `route_engine.py` — networkx graph,
  three route modes (`balanced`, `safest`, `fastest`).
- New endpoints: `/risk/scores`, `/route?from_node_id=&to_node_id=&mode=`.

**Verified behavior:** the model correctly ranks the hilly stretch
(Byrnihat–Nongpoh–Umsning) 5–8x riskier than the flat approach from
Guwahati — `is_monsoon` and `is_hilly` dominate feature importance, as
intended.

**Two known, documented limitations — not bugs, don't "fix" without
re-reading the README first:**
1. All three route modes currently return the identical path. The
   placeholder corridor is 6 nodes in a straight line — no alternate
   route exists for risk-aware routing to choose between. Resolves once
   `fetch_osm_roads.py` loads a real intersection graph. Also a
   legitimate pitch point: single-road dependency is part of the problem.
2. Risk probabilities are small (under 6%) and a 0.5-threshold
   classification report looks weak (recall near 0). Expected — this is a
   training-data-volume limitation, not a modelling mistake. The route
   engine consumes the raw probability as a continuous weight, never a
   0.5 yes/no cutoff, so cite ROC-AUC and relative segment ranking, not
   threshold accuracy.

### Not started yet

- GIS accessibility index + heatmap (member 3)
- Real-time GPS pub/sub + alert engine, push/SMS wiring (member 4)
- Web dashboard (member 5)
- Mobile field-reporting app with offline sync (member 6)
- Actually running `fetch_osm_roads.py` / `fetch_weather.py` against real
  data (needs a machine with normal internet — the sandbox this was built
  in cannot reach the Overpass API or OpenWeatherMap)
- Deployment to Render/Railway/AWS

## How to run it

See `backend/README.md` — it's the source of truth for setup commands,
kept in sync with what was actually run and tested. Quick version:

```bash
docker compose up -d                         # Postgres+PostGIS, Redis
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export PYTHONPATH=$(pwd)
python -m app.scripts.init_db
python -m app.scripts.load_sample_roads
python -m app.scripts.seed_synthetic_data
python -m app.ml.train_risk_model
python -m app.ml.score_segments
uvicorn app.main:app --reload                # http://localhost:8000/docs
```

## Conventions worth keeping

- Every table/response that could be real or placeholder data carries an
  `is_synthetic` flag — don't silently drop this when real data lands.
- Writes that other modules will hook into (weather ingest, vehicle
  position updates) go through an API endpoint, not a direct DB write from
  the fetch script — this is the choke point Phase 2's alert engine and
  real-time broadcast are meant to attach to.
- `risk_scores` / `accessibility_scores` / `alerts` tables exist already,
  empty, specifically so downstream modules don't need a migration to
  start writing to them.

## Roadmap (from the team plan)

Phase 0 (done): scope, repo, stack. Phase 1 (done): backend foundation.
Phase 2 (in progress): route engine + risk model done; accessibility
index, alert engine, real-time GPS pub/sub still open. Phase 3: wire
mobile + dashboard to the live backend, test offline sync, deploy to
staging. Phase 4: end-to-end scenario testing, pitch deck, rehearsal.

Full team plan with day-by-day breakdown, tool/data source list, and the
10-slide pitch outline exists as a separate document from earlier in this
project's planning — ask if you need it reconstructed.
