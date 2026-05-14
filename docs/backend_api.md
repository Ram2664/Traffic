# Backend API (FastAPI)

Base app module: `backend.main:app`

## Endpoints

- `POST /api/load-city` — load city by `city_name` or `bbox`
- `POST /api/centrality` — compute node centralities and rankings
- `POST /api/failure` — run random or targeted initial failures
- `POST /api/cascade` — propagate cascading overload failures
- `POST /api/recovery` — run adaptive recovery strategy
- `GET /api/metrics` — fetch resilience metrics and composite index
- `GET /api/visualization` — fetch visualization-ready node/edge/timeline payload

## Reproducibility and Logs

- Use `seed` fields in request models for deterministic behavior.
- Simulation events are appended to `results/simulation_log.jsonl`.
- Reports are exported under `results/<city_or_bbox>/`.

## Gemini Scaffold

Optional AI scaffold is in `backend/ai/gemini_service.py`.
Set `GEMINI_API_KEY` in `.env` (see `.env.example`).
