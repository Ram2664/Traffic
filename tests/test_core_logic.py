import unittest

import networkx as nx

from backend.cascade.engine import run_cascade
from backend.resilience_index.composite import compute_composite_resilience_index
from backend.simulation.centrality import compute_centrality


class CoreLogicTests(unittest.TestCase):
    def test_centrality_dataframe_has_expected_columns(self):
        graph = nx.path_graph(5)
        centrality_df = compute_centrality(graph)
        self.assertIn('degree', centrality_df.columns)
        self.assertIn('betweenness', centrality_df.columns)
        self.assertIn('closeness', centrality_df.columns)
        self.assertIn('eigenvector', centrality_df.columns)
        for column in ['degree', 'betweenness', 'closeness', 'eigenvector']:
            self.assertTrue(((centrality_df[column] >= 0) & (centrality_df[column] <= 1)).all())

    def test_cascade_propagates_under_overload(self):
        graph = nx.path_graph(3)
        for node in graph.nodes:
            graph.nodes[node].update(
                {
                    'current_load': 10.0,
                    'capacity': 1.0,
                    'overload_threshold': 1.0,
                    'status': 'active',
                }
            )

        result = run_cascade(
            graph=graph,
            initial_failed_nodes=[1],
            redistribution_ratio=1.0,
            overload_threshold=1.0,
            propagation_limit=3,
        )

        self.assertGreaterEqual(len(result['failed_nodes']), 2)
        self.assertGreaterEqual(result['cascade_depth'], 1)

    def test_composite_resilience_index_within_bounds(self):
        metrics = {
            'lcc_ratio': 0.8,
            'global_efficiency': 0.7,
            'recovery_efficiency': 0.5,
            'connectivity_loss': 0.2,
            'failure_ratio': 0.3,
        }
        score = compute_composite_resilience_index(metrics)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


if __name__ == '__main__':
    unittest.main()
