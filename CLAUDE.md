# CLAUDE.md — UrbanFlow AI (Smart India Hackathon)

This file is project memory for Claude Code. Drop it at the root of the
repo (next to `backend/`) and Claude Code will load it automatically at
the start of every session in this project.

## What this is

Smart India Hackathon project: "UrbanFlow AI — Intelligent Urban Transportation, Logistics & Accessibility Platform."

Expected solution per the problem statement: AI route prediction/optimization, GIS accessibility dashboard, GPS vehicle tracking, real-time alerts, mobile/web field reporting, weather/transport/government API integration, cloud infra with offline support.

## Scope decision (locked in, don't relitigate without reason)

Building one pilot corridor end to end for real rather than a shallow
pass at a whole city. **Pilot corridor: Guwahati–Shillong (NH40 / GS
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
