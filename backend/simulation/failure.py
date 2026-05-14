from __future__ import annotations

import random

import networkx as nx


def active_nodes(graph: nx.Graph) -> list:
    return [node for node, attrs in graph.nodes(data=True) if attrs.get('status', 'active') != 'failed']


def choose_failed_nodes(
    graph: nx.Graph,
    strategy: str,
    attack_size: int,
    seed: int,
    centrality_metric: str = 'betweenness',
) -> list:
    attack_size = max(0, min(attack_size, graph.number_of_nodes()))
    nodes = active_nodes(graph)
    if strategy == 'random':
        rng = random.Random(seed)
        return rng.sample(nodes, k=min(attack_size, len(nodes)))

    if strategy == 'targeted_degree':
        ranked = sorted(nodes, key=lambda n: graph.degree(n), reverse=True)
        return ranked[:attack_size]

    if strategy == 'targeted_traffic':
        ranked = sorted(nodes, key=lambda n: graph.nodes[n].get('traffic_load', 0.0), reverse=True)
        return ranked[:attack_size]

    if strategy == 'targeted_centrality':
        ranked = sorted(
            nodes,
            key=lambda n: graph.nodes[n].get('centrality_scores', {}).get(centrality_metric, 0.0),
            reverse=True,
        )
        return ranked[:attack_size]

    raise ValueError(f'Unsupported failure strategy: {strategy}')


def apply_failure(graph: nx.Graph, failed_nodes: list) -> None:
    for node in failed_nodes:
        if node in graph.nodes:
            graph.nodes[node]['status'] = 'failed'
