"""Dijkstra shortest paths for nonnegative road distances."""

import heapq
from math import inf


def shortest_paths(graph: dict[str, list[tuple[str, int]]], source: str
                   ) -> tuple[dict[str, float], dict[str, str | None]]:
    if source not in graph:
        raise ValueError(f"Unknown location: {source}")
    distances: dict[str, float] = {node: inf for node in graph}
    previous: dict[str, str | None] = {node: None for node in graph}
    distances[source] = 0
    heap: list[tuple[int, str]] = [(0, source)]
    while heap:
        distance, node = heapq.heappop(heap)
        if distance != distances[node]:
            continue
        for neighbor, road_distance in graph[node]:
            candidate = distance + road_distance
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = node
                heapq.heappush(heap, (candidate, neighbor))
    return distances, previous


def reconstruct_path(previous: dict[str, str | None], source: str, target: str) -> list[str]:
    if target not in previous:
        raise ValueError(f"Unknown location: {target}")
    path: list[str] = []
    current: str | None = target
    while current is not None:
        path.append(current)
        if current == source:
            return list(reversed(path))
        current = previous[current]
    raise ValueError(f"No route exists from {source} to {target}.")
