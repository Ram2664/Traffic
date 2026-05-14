from __future__ import annotations

from datetime import UTC, datetime
from typing import NoReturn

from fastapi import APIRouter, HTTPException

from backend.api.schemas import CascadeRequest, CentralityRequest, FailureRequest, LoadCityRequest, RecoveryRequest
from backend.api.state import SIM_STATE, STATE_LOCK, artifact_base, ensure_loaded_graph
from backend.cascade.engine import run_cascade
from backend.digital_twin.generator import generate_digital_twin
from backend.experiments.runner import save_experiment_report
from backend.metrics.resilience import compute_resilience_metrics
from backend.recovery.optimizer import run_recovery
from backend.resilience_index.composite import compute_composite_resilience_index
from backend.simulation.centrality import compute_centrality, top_nodes
from backend.simulation.failure import apply_failure, choose_failed_nodes
from backend.utils.io_utils import save_dataframe, save_graph, save_json
from backend.utils.logging_utils import append_jsonl
from backend.utils.reproducibility import set_global_seed
from backend.utils.settings import get_settings
from backend.visualization.prep import prepare_visualization_payload

router = APIRouter(prefix='/api', tags=['simulation'])
logger_name = 'backend.api.routes'


def _handle_error(exc: Exception) -> NoReturn:
    if isinstance(exc, HTTPException):
        raise exc
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if isinstance(exc, FileNotFoundError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=500, detail=f'Internal server error ({logger_name}).') from exc


@router.post('/load-city')
def load_city(request: LoadCityRequest) -> dict:
    settings = get_settings()
    try:
        set_global_seed(request.seed)
        bbox = (
            request.bbox.north,
            request.bbox.south,
            request.bbox.east,
            request.bbox.west,
        ) if request.bbox else None
        artifacts = generate_digital_twin(
            city_name=request.city_name,
            bbox=bbox,
            network_type=request.network_type,
            seed=request.seed,
            capacity_factor=request.capacity_factor,
            overload_threshold=request.overload_threshold,
            speed_mps=request.speed_mps,
        )

        with STATE_LOCK:
            SIM_STATE.graph = artifacts.graph
            SIM_STATE.node_df = artifacts.node_df
            SIM_STATE.edge_df = artifacts.edge_df
            SIM_STATE.city_name = request.city_name or 'bbox'

        base = artifact_base(settings.results_dir)
        save_graph(artifacts.graph, base / 'graph.gpickle')
        save_dataframe(artifacts.node_df, base / 'nodes.csv')
        save_dataframe(artifacts.edge_df, base / 'edges.csv')
        save_json(artifacts.visualization_json, base / 'visualization.json')

        append_jsonl(
            settings.results_dir / 'simulation_log.jsonl',
            {
                'event': 'load_city',
                'city': SIM_STATE.city_name,
                'nodes': artifacts.graph.number_of_nodes(),
                'edges': artifacts.graph.number_of_edges(),
                'seed': request.seed,
            },
        )

        return {
            'status': 'loaded',
            'city': SIM_STATE.city_name,
            'node_count': artifacts.graph.number_of_nodes(),
            'edge_count': artifacts.graph.number_of_edges(),
            'artifacts': {
                'graph': str(base / 'graph.gpickle'),
                'nodes_csv': str(base / 'nodes.csv'),
                'edges_csv': str(base / 'edges.csv'),
                'visualization_json': str(base / 'visualization.json'),
            },
        }
    except Exception as exc:
        return _handle_error(exc)


@router.post('/centrality')
def centrality(request: CentralityRequest) -> dict:
    settings = get_settings()
    try:
        with STATE_LOCK:
            graph = ensure_loaded_graph()
        centrality_df = compute_centrality(graph)
        with STATE_LOCK:
            SIM_STATE.last_centrality = centrality_df

        base = artifact_base(settings.results_dir)
        save_dataframe(centrality_df, base / 'centrality.csv')

        return {
            'status': 'ok',
            'generated_at': datetime.now(UTC).isoformat(),
            'top_nodes': top_nodes(centrality_df, n=request.top_n),
            'report_csv': str(base / 'centrality.csv'),
        }
    except Exception as exc:
        return _handle_error(exc)


@router.post('/failure')
def failure(request: FailureRequest) -> dict:
    settings = get_settings()
    try:
        with STATE_LOCK:
            graph = ensure_loaded_graph()
        selected = choose_failed_nodes(
            graph=graph,
            strategy=request.strategy,
            attack_size=request.attack_size,
            seed=request.seed,
            centrality_metric=request.centrality_metric,
        )
        apply_failure(graph, selected)
        metrics = compute_resilience_metrics(graph)

        payload = {
            'failed_nodes': [str(node) for node in selected],
            'strategy': request.strategy,
            'metrics': metrics,
        }
        with STATE_LOCK:
            SIM_STATE.last_failure = payload

        append_jsonl(settings.results_dir / 'simulation_log.jsonl', {'event': 'failure', **payload})
        save_experiment_report([payload], artifact_base(settings.results_dir) / 'failure_report.csv')
        return payload
    except Exception as exc:
        return _handle_error(exc)


@router.post('/cascade')
def cascade(request: CascadeRequest) -> dict:
    settings = get_settings()
    try:
        with STATE_LOCK:
            graph = ensure_loaded_graph()
        initial_failed = [n for n, attrs in graph.nodes(data=True) if attrs.get('status') == 'failed']
        result = run_cascade(
            graph=graph,
            initial_failed_nodes=initial_failed,
            redistribution_ratio=request.redistribution_ratio,
            overload_threshold=request.overload_threshold,
            propagation_limit=request.propagation_limit,
        )
        metrics = compute_resilience_metrics(graph)
        result['metrics'] = metrics

        with STATE_LOCK:
            SIM_STATE.last_cascade = result
        append_jsonl(settings.results_dir / 'simulation_log.jsonl', {'event': 'cascade', **result})
        save_json(result, artifact_base(settings.results_dir) / 'cascade_report.json')
        return result
    except Exception as exc:
        return _handle_error(exc)


@router.post('/recovery')
def recovery(request: RecoveryRequest) -> dict:
    settings = get_settings()
    try:
        with STATE_LOCK:
            graph = ensure_loaded_graph()
        result = run_recovery(graph, request.strategy, request.steps, request.seed)
        metrics = compute_resilience_metrics(graph)
        score = compute_composite_resilience_index(metrics)
        result['metrics'] = metrics
        result['composite_resilience_index'] = score

        with STATE_LOCK:
            SIM_STATE.last_recovery = result
        append_jsonl(settings.results_dir / 'simulation_log.jsonl', {'event': 'recovery', **result})
        save_json(result, artifact_base(settings.results_dir) / 'recovery_report.json')
        return result
    except Exception as exc:
        return _handle_error(exc)


@router.get('/metrics')
def metrics() -> dict:
    try:
        with STATE_LOCK:
            graph = ensure_loaded_graph()
        metric_values = compute_resilience_metrics(graph)
        metric_values['composite_resilience_index'] = compute_composite_resilience_index(metric_values)
        return metric_values
    except Exception as exc:
        return _handle_error(exc)


@router.get('/visualization')
def visualization() -> dict:
    try:
        with STATE_LOCK:
            graph = ensure_loaded_graph()
            timeline = SIM_STATE.last_cascade.get('timeline', []) if SIM_STATE.last_cascade else []
        return prepare_visualization_payload(graph, timeline)
    except Exception as exc:
        return _handle_error(exc)
