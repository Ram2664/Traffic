from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import networkx as nx
import pandas as pd


@dataclass
class SimulationState:
    graph: nx.Graph | None = None
    node_df: pd.DataFrame | None = None
    edge_df: pd.DataFrame | None = None
    city_name: str | None = None
    last_centrality: pd.DataFrame | None = None
    last_failure: dict = field(default_factory=dict)
    last_cascade: dict = field(default_factory=dict)
    last_recovery: dict = field(default_factory=dict)


SIM_STATE = SimulationState()


def ensure_loaded_graph() -> nx.Graph:
    if SIM_STATE.graph is None:
        raise ValueError('No city graph loaded. Call /api/load-city first.')
    return SIM_STATE.graph


def artifact_base(results_dir: Path) -> Path:
    city = (SIM_STATE.city_name or 'bbox').replace(' ', '_').replace(',', '_')
    return results_dir / city
