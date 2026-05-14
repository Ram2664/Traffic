from __future__ import annotations

import networkx as nx


def run_cascade(
    graph: nx.Graph,
    initial_failed_nodes: list,
    redistribution_ratio: float,
    overload_threshold: float,
    propagation_limit: int,
) -> dict:
    for node in initial_failed_nodes:
        if node in graph.nodes:
            graph.nodes[node]['status'] = 'failed'

    timeline: list[dict] = []
    frontier = set(initial_failed_nodes)
    all_failed = set(initial_failed_nodes)

    for depth in range(1, propagation_limit + 1):
        newly_failed: set = set()
        for failed_node in frontier:
            if failed_node not in graph.nodes:
                continue
            neighbors = [n for n in graph.neighbors(failed_node) if graph.nodes[n].get('status', 'active') != 'failed']
            if not neighbors:
                continue

            redistributed = graph.nodes[failed_node].get('current_load', 0.0) * redistribution_ratio
            load_increment = redistributed / len(neighbors)

            for neighbor in neighbors:
                graph.nodes[neighbor]['current_load'] = graph.nodes[neighbor].get('current_load', 0.0) + load_increment
                cap = graph.nodes[neighbor].get('capacity', 0.0)
                thresh = graph.nodes[neighbor].get('overload_threshold', overload_threshold)
                if graph.nodes[neighbor]['current_load'] > cap * thresh:
                    graph.nodes[neighbor]['status'] = 'failed'
                    newly_failed.add(neighbor)

        timeline.append({'depth': depth, 'newly_failed_nodes': [str(n) for n in sorted(newly_failed)]})
        if not newly_failed:
            break
        frontier = newly_failed
        all_failed.update(newly_failed)

    return {
        'failed_nodes': [str(n) for n in sorted(all_failed)],
        'cascade_depth': len(timeline),
        'timeline': timeline,
    }
