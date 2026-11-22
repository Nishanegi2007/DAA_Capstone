"""Nearest-neighbor route planning over Dijkstra shortest-path distances."""

from math import inf

from .dijkstra import reconstruct_path, shortest_paths


def plan_route(graph: dict[str, list[tuple[str, int]]], depot: str,
               destinations: list[str]) -> tuple[list[str], int]:
    """Visit unique destinations by nearest neighbor and return to the depot.

    Dijkstra distances make each leg a true shortest road path. The returned
    sequence is the expanded road-by-road route, including the depot at both ends.
    """
    stops = list(dict.fromkeys(destinations))
    if not stops:
        return [depot], 0
    sources = [depot, *stops]
    all_distances = {source: shortest_paths(graph, source)[0] for source in sources}
    current = depot
    remaining = set(stops)
    # Include the depot so the first leg (depot to the first customer) is
    # expanded and counted just like every later leg.
    stop_order: list[str] = [depot]
    while remaining:
        reachable = [(all_distances[current].get(stop, inf), stop) for stop in remaining]
        distance, next_stop = min(reachable)
        if distance == inf:
            raise ValueError(f"Some destinations are unreachable from {current}.")
        stop_order.append(next_stop)
        remaining.remove(next_stop)
        current = next_stop
    stop_order.append(depot)

    full_route: list[str] = [depot]
    total_distance = 0
    for start, end in zip(stop_order, stop_order[1:]):
        leg_distance = all_distances[start].get(end, inf)
        if leg_distance == inf:
            raise ValueError(f"No route exists from {start} to {end}.")
        leg = reconstruct_path(shortest_paths(graph, start)[1], start, end)
        full_route.extend(leg[1:])
        total_distance += int(leg_distance)
    return full_route, total_distance
