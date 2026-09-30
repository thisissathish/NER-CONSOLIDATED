# Implementation Plan: Transform to UrbanFlow AI

## Context
The goal is to transition the "NER Smart Logistics" prototype into "UrbanFlow AI", a city-agnostic urban transportation and logistics intelligence platform. This will allow the platform to be easily configured for any city or region by removing hardcoded geographic constraints, updating branding, and generalizing documentation.

## Proposed Strategy

### Phase 1: Identity & Branding Refactoring
- Rename project-wide references from "NER Smart Logistics" to "UrbanFlow AI".
- Update front-end branding in `dashboard.html`.
- Update API titles and versioning in `backend/app/main.py` and `backend/app/config.py`.
- Update `README.md` and related docs.

### Phase 2: Geographic Generalization
- Replace hardcoded corridor bounds in `backend/app/config.py` with configurable environment variables (e.g., `DEFAULT_CITY_NAME`, `CITY_MIN_LAT`, etc.).
- Update `backend/app/scripts/fetch_osm_roads.py` to use these environment variables instead of hardcoded NER coordinates.
- Ensure `backend/.env.example` includes these new generalized variables.

### Phase 3: Documentation & Metadata Update
- Update all `.md` files to reflect the new global identity.
- Preserve technical details of implemented algorithms, ensuring "AI" descriptions are accurate (e.g., emphasizing XGBoost vs. Graph algorithms).
- Mark NER-based files as examples/demos if kept.

### Phase 4: Risk Mitigation & Validation
- Run `backend_test.py` to ensure core API endpoints (Roads, Vehicles, Routing) remain functional.
- Validate that the dashboard still loads and interacts with the API.
- Do NOT delete existing sample data scripts (`load_sample_roads.py`, `seed_synthetic_data.py`), but update them to be clearly labeled as demos.

## Critical Files to be Modified
- `CLAUDE.md`
- `README.md`
- `backend/README.md`
- `backend/app/config.py`
- `backend/app/main.py`
- `backend/app/scripts/fetch_osm_roads.py`
- `dashboard.html`
- `backend/.env.example`
- Various documentation files (`QUICKSTART.md`, etc.)

## Verification
1. Run `pytest` if supported, or manually run `backend_test.py`.
2. Inspect `http://localhost:8000/docs` to verify generalized API titles/descriptions.
3. Launch `dashboard.html` and verify UI branding.
4. Verify environment variable loading.
