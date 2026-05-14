from fastapi import FastAPI

from backend.api.routes import router
from backend.utils.logging_utils import configure_logging
from backend.utils.settings import get_settings

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title='Digital Twin Transportation Resilience Backend',
    description='Backend for cascading failure modeling and adaptive resilience optimization.',
    version='1.0.0',
)
app.include_router(router)


@app.get('/health')
def health() -> dict:
    return {'status': 'ok', 'environment': settings.app_env}
