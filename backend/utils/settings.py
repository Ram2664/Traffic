from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Traffic Digital Twin Backend'
    app_env: str = 'development'
    log_level: str = 'INFO'

    data_dir: Path = Field(default=Path('data'))
    results_dir: Path = Field(default=Path('results'))
    docs_dir: Path = Field(default=Path('docs'))

    default_network_type: str = 'drive'
    default_speed_mps: float = 11.11
    default_capacity_factor: float = 1.5
    default_overload_threshold: float = 1.2
    default_redistribution_ratio: float = 0.5
    default_seed: int = 42

    gemini_api_key: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.results_dir.mkdir(parents=True, exist_ok=True)
    settings.docs_dir.mkdir(parents=True, exist_ok=True)
    return settings
