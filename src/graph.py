"""Undirected weighted road graph helpers."""

from collections import defaultdict

from .models import Road


def build_graph(roads: list[Road]) -> dict[str, list[tuple[str, int]]]:
    graph: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for start, end, distance in roads:
        graph[start].append((end, distance))
        graph[end].append((start, distance))
    return dict(graph)
