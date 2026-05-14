import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def configure_logging(level: str = 'INFO') -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    enriched = {'timestamp': datetime.now(UTC).isoformat(), **payload}
    with path.open('a', encoding='utf-8') as file:
        file.write(json.dumps(enriched) + '\n')
