"""Dijkstra's algorithm for a weighted graph."""

from collections import deque
from typing import List, Optional, Tuple

from datastructures import PriorityQueue


class SimpleGraph:
    """Simple weighted, directed graph implementation.

    Only one of size and adj_mat can be set. when size is specified, a graph of
    disconnected nodes is initialized. `adj_mat` is not validated.

    Parameters:
        size: The number of nodes in the graph
        adj_mat: An adjacency matrix filled with integer weights where there is
            an edge and zeros where there is no edge

    """

    def __init__(
        self, size: Optional[int] = None, adj_mat: Optional[List[List[int]]] = None
    ):
        if size is not None and adj_mat is not None:
            raise ValueError("only one of size and adj_mat is allowed")
        if adj_mat is not None:
            self.adj_mat = adj_mat
            self.size = len(adj_mat)
        elif size is not None:
            self.adj_mat = [[0] * size for _ in range(size)]
            self.size = size
        else:
            raise ValueError("one of size and adj_mat must be specified")

    def set_edge_weight(
        self, source: int, target: int, weight: int, directed: bool = False
    ):
        self.adj_mat[source][target] = weight
        if not directed:
            self.adj_mat[target][source] = weight

    def dijkstra_path(self, source: int) -> Tuple[List[float], List[Optional[int]]]:
        dist = [float("inf") for _ in range(self.size)]
        prev = [None for _ in range(self.size)]
        dist[source] = 0
        pq = PriorityQueue(list(range(self.size)), dist)  # O(n)
        visited = set()

        while pq:
            node = pq.extract_root()
            visited.add(node)
            for neighbor in range(self.size):
                weight = self.adj_mat[node][neighbor]
                # skip over neighbors already visited or that aren't actually
                # neighbors (edge weight zero)
                if neighbor in visited or weight == 0:
                    continue
                else:
                    alt = dist[node] + weight
                    if alt < dist[neighbor]:
                        dist[neighbor] = alt
                        prev[neighbor] = node
                        pq.update_value_priority(neighbor, alt)  # O(log(n))

        return dist, prev

    @staticmethod
    def shortest_path(source: int, target: int, prev: List[int]):
        seq = deque()
        u = target
        if prev[u] is not None or u == source:
            while u is not None:
                seq.appendleft(u)
                u = prev[u]

        return seq

    def visualize(self):  # pragma: no cover
        try:
            import matplotlib.pyplot as plt
            import networkx as nx
            import numpy as np

            G = nx.from_numpy_matrix(np.array(self.adj_mat))
            # requires graphviz installation
            pos = nx.nx_agraph.graphviz_layout(G)
            # note: you need to manually hint to networkx, when the graph is directed
            #       to specify which edges are actually directed vs undirected
            nx.draw_networkx(G, pos)
            labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            plt.show()
        except ImportError:  # pragma: no cover
            raise ValueError("please install the [graph] extras")
