from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np
import pandas as pd

from backend.digital_twin.models import DigitalTwinArtifacts


def _normalize_graph(graph: nx.MultiDiGraph) -> nx.Graph:
    normalized = nx.Graph()
    for node_id, attrs in graph.nodes(data=True):
        normalized.add_node(node_id, **attrs)
    for u, v, attrs in graph.edges(data=True):
        if normalized.has_edge(u, v):
            continue
        normalized.add_edge(u, v, **attrs)
    return normalized


def _compute_edge_weight(length: float, congestion_level: float) -> float:
    return float(length) * max(congestion_level, 0.1)


def assign_transport_attributes(
    graph: nx.Graph,
    seed: int,
    capacity_factor: float,
    overload_threshold: float,
    speed_mps: float,
) -> nx.Graph:
    rng = np.random.default_rng(seed)
    for node_id, attrs in graph.nodes(data=True):
        traffic_load = float(rng.uniform(1.0, 10.0))
        attrs.update(
            {
                'node_id': str(node_id),
                'latitude': float(attrs.get('y', 0.0)),
                'longitude': float(attrs.get('x', 0.0)),
                'traffic_load': traffic_load,
                'capacity': traffic_load * capacity_factor,
                'current_load': traffic_load,
                'overload_threshold': overload_threshold,
                'status': 'active',
                'centrality_scores': {},
            }
        )

    for _, _, attrs in graph.edges(data=True):
        distance = float(attrs.get('length', 1.0))
        road_type = attrs.get('highway', 'unclassified')
        road_type = road_type[0] if isinstance(road_type, list) and road_type else str(road_type or 'unclassified')
        congestion_level = float(attrs.get('congestion_level', 1.0))
        travel_time = distance / max(speed_mps, 0.1)
        attrs.update(
            {
                'distance': distance,
                'travel_time': travel_time,
                'road_type': str(road_type),
                'congestion_level': congestion_level,
                'edge_weight': _compute_edge_weight(distance, congestion_level),
            }
        )
    return graph


def graph_to_dataframes(graph: nx.Graph) -> tuple[pd.DataFrame, pd.DataFrame]:
    node_records: list[dict[str, Any]] = []
    for node_id, attrs in graph.nodes(data=True):
        node_records.append({'node_id': str(node_id), **attrs})

    edge_records: list[dict[str, Any]] = []
    for u, v, attrs in graph.edges(data=True):
        edge_records.append({'source': str(u), 'target': str(v), **attrs})

    return pd.DataFrame(node_records), pd.DataFrame(edge_records)


def build_visualization_json(graph: nx.Graph) -> dict[str, Any]:
    nodes = [
        {
            'id': str(node_id),
            'lat': attrs.get('latitude', attrs.get('y')),
            'lon': attrs.get('longitude', attrs.get('x')),
            'status': attrs.get('status', 'active'),
            'current_load': attrs.get('current_load', 0.0),
        }
        for node_id, attrs in graph.nodes(data=True)
    ]
    edges = [
        {
            'source': str(u),
            'target': str(v),
            'distance': attrs.get('distance', attrs.get('length', 1.0)),
            'edge_weight': attrs.get('edge_weight', 1.0),
        }
        for u, v, attrs in graph.edges(data=True)
    ]
    return {'nodes': nodes, 'edges': edges}


def generate_digital_twin(
    city_name: str | None,
    bbox: tuple[float, float, float, float] | None,
    network_type: str,
    seed: int,
    capacity_factor: float,
    overload_threshold: float,
    speed_mps: float,
) -> DigitalTwinArtifacts:
    try:
        import osmnx as ox
    except ImportError as exc:
        raise RuntimeError('OSMnx is required to load real OSM city data.') from exc

    if city_name:
        base_graph = ox.graph_from_place(city_name, network_type=network_type, simplify=True)
    elif bbox:
        north, south, east, west = bbox
        base_graph = ox.graph_from_bbox(
            north=north,
            south=south,
            east=east,
            west=west,
            network_type=network_type,
            simplify=True,
        )
    else:
        raise ValueError('Either city_name or bbox must be provided.')

    graph = _normalize_graph(base_graph)
    graph = assign_transport_attributes(graph, seed, capacity_factor, overload_threshold, speed_mps)
    node_df, edge_df = graph_to_dataframes(graph)
    visualization_json = build_visualization_json(graph)
    return DigitalTwinArtifacts(graph=graph, node_df=node_df, edge_df=edge_df, visualization_json=visualization_json)
