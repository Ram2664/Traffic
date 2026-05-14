from __future__ import annotations

import random

import networkx as nx

from backend.metrics.resilience import compute_resilience_metrics


STRATEGIES = {'random', 'high_traffic_first', 'critical_node_first', 'hybrid'}


def _candidate_failed_nodes(graph: nx.Graph) -> list:
    return [node for node, attrs in graph.nodes(data=True) if attrs.get('status') == 'failed']


def _strategy_order(graph: nx.Graph, failed_nodes: list, strategy: str, seed: int) -> list:
    if strategy == 'random':
        rng = random.Random(seed)
        nodes = failed_nodes[:]
        rng.shuffle(nodes)
        return nodes

    if strategy == 'high_traffic_first':
        return sorted(failed_nodes, key=lambda n: graph.nodes[n].get('traffic_load', 0.0), reverse=True)

    if strategy == 'critical_node_first':
        return sorted(
            failed_nodes,
            key=lambda n: graph.nodes[n].get('centrality_scores', {}).get('betweenness', 0.0),
            reverse=True,
        )

    if strategy == 'hybrid':
        return sorted(
            failed_nodes,
            key=lambda n: (
                graph.nodes[n].get('traffic_load', 0.0)
                + graph.nodes[n].get('centrality_scores', {}).get('betweenness', 0.0)
                + graph.degree(n)
            ),
            reverse=True,
        )

    raise ValueError(f'Unsupported recovery strategy: {strategy}')


def run_recovery(graph: nx.Graph, strategy: str, steps: int, seed: int) -> dict:
    if strategy not in STRATEGIES:
        raise ValueError(f'Unsupported recovery strategy: {strategy}')

    failed = _candidate_failed_nodes(graph)
    order = _strategy_order(graph, failed, strategy, seed)
    timeline = []

    for step in range(1, steps + 1):
        if not order:
            break
        recovered = order.pop(0)
        graph.nodes[recovered]['status'] = 'recovered'
        graph.nodes[recovered]['current_load'] = graph.nodes[recovered].get('traffic_load', 0.0)

        metrics = compute_resilience_metrics(graph)
        timeline.append({'step': step, 'recovered_node': str(recovered), 'metrics': metrics})

    return {
        'strategy': strategy,
        'timeline': timeline,
        'remaining_failed_nodes': [str(node) for node in order],
        'recovered_nodes': [event['recovered_node'] for event in timeline],
    }
