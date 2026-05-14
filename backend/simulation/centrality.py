from __future__ import annotations

from typing import Iterable

import networkx as nx
import pandas as pd


def normalize_scores(scores: dict) -> dict:
    if not scores:
        return {}
    min_val = min(scores.values())
    max_val = max(scores.values())
    if max_val == min_val:
        return {k: 0.5 for k in scores}
    return {k: (v - min_val) / (max_val - min_val) for k, v in scores.items()}


def compute_centrality(graph: nx.Graph) -> pd.DataFrame:
    degree = normalize_scores(nx.degree_centrality(graph))
    betweenness = normalize_scores(nx.betweenness_centrality(graph, normalized=True))
    closeness = normalize_scores(nx.closeness_centrality(graph))
    try:
        eigenvector_raw = nx.eigenvector_centrality(graph, max_iter=1000)
    except nx.NetworkXException:
        eigenvector_raw = {node: 0.0 for node in graph.nodes}
    eigenvector = normalize_scores(eigenvector_raw)

    records = []
    for node in graph.nodes:
        scores = {
            'degree': float(degree.get(node, 0.0)),
            'betweenness': float(betweenness.get(node, 0.0)),
            'closeness': float(closeness.get(node, 0.0)),
            'eigenvector': float(eigenvector.get(node, 0.0)),
        }
        graph.nodes[node]['centrality_scores'] = scores
        records.append({'node_id': str(node), **scores, 'composite_rank_score': sum(scores.values()) / 4.0})

    centrality_df = pd.DataFrame(records).sort_values(by='composite_rank_score', ascending=False).reset_index(drop=True)
    centrality_df['rank'] = centrality_df.index + 1
    return centrality_df


def top_nodes(centrality_df: pd.DataFrame, n: int = 10) -> list[dict]:
    return centrality_df.head(n).to_dict(orient='records')


def node_ids_by_metric(centrality_df: pd.DataFrame, metric: str, count: int) -> Iterable[str]:
    return centrality_df.sort_values(metric, ascending=False).head(count)['node_id'].tolist()
