from dataclasses import dataclass

import networkx as nx
import pandas as pd


@dataclass
class DigitalTwinArtifacts:
    graph: nx.Graph
    node_df: pd.DataFrame
    edge_df: pd.DataFrame
    visualization_json: dict
