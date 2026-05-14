from __future__ import annotations

import networkx as nx


def prepare_visualization_payload(graph: nx.Graph, timeline: list[dict] | None = None) -> dict:
    nodes = []
    for node_id, attrs in graph.nodes(data=True):
        nodes.append(
            {
                'id': str(node_id),
                'lat': attrs.get('latitude', attrs.get('y')),
                'lon': attrs.get('longitude', attrs.get('x')),
                'status': attrs.get('status', 'active'),
                'traffic_load': attrs.get('traffic_load', 0.0),
                'current_load': attrs.get('current_load', 0.0),
                'capacity': attrs.get('capacity', 0.0),
            }
        )

    edges = []
    for u, v, attrs in graph.edges(data=True):
        edges.append(
            {
                'source': str(u),
                'target': str(v),
                'distance': attrs.get('distance', attrs.get('length', 0.0)),
                'travel_time': attrs.get('travel_time', 0.0),
                'road_type': attrs.get('road_type', 'unknown'),
                'edge_weight': attrs.get('edge_weight', 1.0),
            }
        )

    return {
        'nodes': nodes,
        'edges': edges,
        'timeline': timeline or [],
        'summary': {
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'failed_nodes': sum(1 for n in nodes if n['status'] == 'failed'),
            'recovered_nodes': sum(1 for n in nodes if n['status'] == 'recovered'),
        },
    }
