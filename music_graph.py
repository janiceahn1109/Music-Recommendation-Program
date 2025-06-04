"""music_graph.py

This module defines the music graph structure for representing songs and their similarities.
This module includes the _Vertex and MusicGraph classes, which enable graph construction, similarity computation,
as well as the visualization of song relationships based on musical features.
"""

from __future__ import annotations
from typing import Any, Dict
import doctest
import python_ta
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class _Vertex:
    """A class representing a song vertex in the graph.

    >>> v1 = _Vertex('Song A', [0.2, 0.4])
    >>> v2 = _Vertex('Song B', [0.1, 0.5])
    >>> round(v1.similarity_score(v2), 2)
    0.22
    >>> v1.add_edge(v2, 0.22)
    >>> v2.item in v1.neighbours
    True
    """

    item: Any
    values: list[float]
    neighbours: dict[Any, float]

    def __init__(self, item: Any, values: list[float]) -> None:
        """Initialize a _Vertex with an item and its feature values."""
        self.item = item
        self.values = values
        self.neighbours = {}

    def add_edge(self, other: _Vertex, weight: float) -> None:
        """Add a bidirectional edge with a weight to another vertex."""
        self.neighbours[other.item] = weight
        other.neighbours[self.item] = weight

    def similarity_score(self, other: _Vertex) -> float:
        """Return the similarity score between this and another vertex.

        >>> v1 = _Vertex('Song A', [0.2, 0.4])
        >>> v2 = _Vertex('Song B', [0.1, 0.5])
        >>> round(v1.similarity_score(v2), 2)
        0.22
        """
        return float(np.dot(self.values, other.values))


class MusicGraph:
    """A class representing a music similarity graph.

    >>> graph = MusicGraph()
    >>> graph.add_vertex('Song A', [0.2, 0.4])
    >>> graph.add_vertex('Song B', [0.1, 0.5])
    >>> graph.add_edge('Song A', 'Song B', 0.22)
    >>> round(graph.get_similarity_score('Song A', 'Song B'), 2)
    0.22
    >>> graph.recommend_songs('Song A')
    ['Song B']
    """

    _vertices: Dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty music graph."""
        self._vertices = {}

    def add_vertex(self, item: Any, values: list[float]) -> None:
        """Add a song to the graph."""
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, values)

    def add_edge(self, item1: Any, item2: Any, weight: float) -> None:
        """Add an edge between two songs with the given weight."""
        if item1 in self._vertices and item2 in self._vertices:
            self._vertices[item1].add_edge(self._vertices[item2], weight)

    def get_similarity_score(self, item1: Any, item2: Any) -> float:
        """Return the similarity score between two songs.

        >>> graph = MusicGraph()
        >>> graph.add_vertex('Song A', [0.2, 0.4])
        >>> graph.add_vertex('Song B', [0.1, 0.5])
        >>> round(graph.get_similarity_score('Song A', 'Song B'), 2)
        0.22
        """
        if item1 in self._vertices and item2 in self._vertices:
            return self._vertices[item1].similarity_score(self._vertices[item2])
        raise ValueError("Song(s) not found in graph.")

    def recommend_songs(self, item: Any, limit: int = 5) -> list[str]:
        """Return up to 'limit' most similar songs to the given song."""
        if item not in self._vertices:
            raise ValueError("Song not found in graph.")

        neighbors = self._vertices[item].neighbours.items()
        sorted_neighbors = sorted(neighbors, key=lambda x: -x[1])
        return [song for song, _ in sorted_neighbors][:limit]

    def to_networkx(self) -> nx.Graph:
        """Convert the music graph to a NetworkX graph."""
        graph_nx = nx.Graph()
        for item, vertex in self._vertices.items():
            graph_nx.add_node(item)
            for neighbor, weight in vertex.neighbours.items():
                graph_nx.add_edge(item, neighbor, weight=weight)
        return graph_nx

    def get_figure(self, focus_song: str = None, limit: int = 10) -> plt.Figure:
        """Return a matplotlib Figure object showing the similarity graph.

        If focus_song is provided, only the song and its top 'limit' neighbors are shown.
        """
        graph_nx = self.to_networkx()

        if focus_song and focus_song in graph_nx:
            neighbors_with_weights = [(n, graph_nx[focus_song][n]['weight']) for n in graph_nx.neighbors(focus_song)]
            top_neighbors = sorted(neighbors_with_weights, key=lambda x: -x[1])[:limit]
            sub_nodes = [focus_song] + [n for n, _ in top_neighbors]
            graph_nx = graph_nx.subgraph(sub_nodes)

        pos = nx.spring_layout(graph_nx, seed=42)
        fig, ax = plt.subplots(figsize=(7, 5), dpi=100)

        node_colors = []
        node_sizes = []
        for node in graph_nx.nodes:
            if node == focus_song:
                node_colors.append("red")
                node_sizes.append(600)
            else:
                node_colors.append("#1DB954")
                node_sizes.append(300)

        nx.draw_networkx_nodes(graph_nx, pos, ax=ax, node_color=node_colors, node_size=node_sizes)
        nx.draw_networkx_edges(graph_nx, pos, ax=ax, edge_color="gray", alpha=0.5)
        nx.draw_networkx_labels(graph_nx, pos, ax=ax, font_size=8, font_color="black")

        ax.set_title("Song Similarity Graph", fontsize=14)
        ax.axis("off")

        return fig

        # I used Chat GPT for the get_figure method.


if __name__ == '__main__':
    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['numpy', 'networkx', 'matplotlib.pyplot'],
        'allowed-io': [],
        'max-line-length': 120
    })
