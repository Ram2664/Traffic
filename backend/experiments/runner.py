from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_experiment_report(rows: list[dict], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_path, index=False)
    return output_path
