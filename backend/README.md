# Backend

FastAPI backend for digital twin generation, cascading-failure simulation, resilience metrics, and recovery optimization.

## Run

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## API Endpoints

- `POST /api/load-city`
- `POST /api/centrality`
- `POST /api/failure`
- `POST /api/cascade`
- `POST /api/recovery`
- `GET /api/metrics`
- `GET /api/visualization`
