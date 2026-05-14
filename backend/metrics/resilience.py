from __future__ import annotations

import networkx as nx


def _active_subgraph(graph: nx.Graph) -> nx.Graph:
    active = [n for n, attrs in graph.nodes(data=True) if attrs.get('status', 'active') != 'failed']
    return graph.subgraph(active).copy()


def compute_resilience_metrics(graph: nx.Graph) -> dict[str, float]:
    total_nodes = graph.number_of_nodes()
    failed_nodes = [n for n, attrs in graph.nodes(data=True) if attrs.get('status') == 'failed']
    recovered_nodes = [n for n, attrs in graph.nodes(data=True) if attrs.get('status') == 'recovered']
    active_graph = _active_subgraph(graph)

    if active_graph.number_of_nodes() == 0:
        lcc_size = 0
        avg_path_length = 0.0
        efficiency = 0.0
    else:
        components = list(nx.connected_components(active_graph))
        lcc_size = len(max(components, key=len)) if components else 0
        lcc_graph = active_graph.subgraph(max(components, key=len)).copy() if components else active_graph
        avg_path_length = nx.average_shortest_path_length(lcc_graph) if lcc_graph.number_of_nodes() > 1 else 0.0
        efficiency = nx.global_efficiency(active_graph) if active_graph.number_of_nodes() > 1 else 0.0

    lcc_ratio = (lcc_size / total_nodes) if total_nodes else 0.0
    failure_ratio = (len(failed_nodes) / total_nodes) if total_nodes else 0.0
    connectivity_loss = 1.0 - lcc_ratio
    recovery_efficiency = len(recovered_nodes) / max(1, len(failed_nodes) + len(recovered_nodes))

    return {
        'lcc_ratio': float(lcc_ratio),
        'connectivity_loss': float(connectivity_loss),
        'average_path_length': float(avg_path_length),
        'global_efficiency': float(efficiency),
        'failure_ratio': float(failure_ratio),
        'recovery_efficiency': float(recovery_efficiency),
    }
