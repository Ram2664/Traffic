from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class BoundingBox(BaseModel):
    # Order intentionally matches OSMnx graph_from_bbox signature.
    north: float
    south: float
    east: float
    west: float


class LoadCityRequest(BaseModel):
    city_name: str | None = None
    bbox: BoundingBox | None = None
    network_type: str = 'drive'
    seed: int = 42
    capacity_factor: float = 1.5
    overload_threshold: float = 1.2
    speed_mps: float = 11.11

    @model_validator(mode='after')
    def validate_source(self) -> 'LoadCityRequest':
        if not self.city_name and not self.bbox:
            raise ValueError('Either city_name or bbox must be provided.')
        return self


class CentralityRequest(BaseModel):
    top_n: int = Field(default=10, ge=1)


class FailureRequest(BaseModel):
    strategy: Literal['random', 'targeted_degree', 'targeted_traffic', 'targeted_centrality'] = 'random'
    attack_size: int = Field(default=5, ge=0)
    seed: int = 42
    centrality_metric: str = 'betweenness'


class CascadeRequest(BaseModel):
    redistribution_ratio: float = Field(default=0.5, ge=0.0)
    overload_threshold: float = Field(default=1.2, ge=0.0)
    propagation_limit: int = Field(default=10, ge=1)


class RecoveryRequest(BaseModel):
    strategy: Literal['random', 'high_traffic_first', 'critical_node_first', 'hybrid'] = 'hybrid'
    steps: int = Field(default=5, ge=0)
    seed: int = 42


class CompositeIndexRequest(BaseModel):
    weights: dict[str, float] | None = None
