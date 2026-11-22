"""Small repeatable runtime benchmark and chart generation."""

import csv
import random
import time
from pathlib import Path

from .dijkstra import shortest_paths
from .knapsack import choose_parcels
from .models import Parcel
from .routing import plan_route
from .sorting import merge_sort_parcels


def _timed(callable_, repeats: int = 5) -> float:
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        callable_()
        samples.append(time.perf_counter() - start)
    return sum(samples) / repeats


def run_benchmarks(output_dir: str | Path) -> tuple[Path, Path]:
    rng = random.Random(42)
    rows: list[dict[str, int | float | str]] = []
    for size in (20, 50, 100, 200):
        parcels: list[Parcel] = [{
            "id": f"P{i:04d}", "destination": f"C{i % 12}",
            "weight": rng.randint(100, 1000), "priority": rng.randint(1, 3),
            "deadline_days": rng.randint(1, 30), "value": rng.randint(10, 100),
        } for i in range(size)]
        rows.append({"component": "Merge Sort", "input_size": size,
                     "average_seconds": _timed(lambda: merge_sort_parcels(parcels))})
        rows.append({"component": "0/1 Knapsack DP (capacity 5000)", "input_size": size,
                     "average_seconds": _timed(lambda: choose_parcels(parcels, 5000), repeats=3)})

    for node_count in (20, 50, 100, 200):
        graph = {f"N{i}": [] for i in range(node_count)}
        for i in range(node_count - 1):
            graph[f"N{i}"].append((f"N{i+1}", 1 + (i % 7)))
            graph[f"N{i+1}"].append((f"N{i}", 1 + (i % 7)))
        for i in range(0, node_count - 5, 5):
            graph[f"N{i}"].append((f"N{i+5}", 3))
            graph[f"N{i+5}"].append((f"N{i}", 3))
        rows.append({"component": "Dijkstra", "input_size": node_count,
                     "average_seconds": _timed(lambda g=graph: shortest_paths(g, "N0"))})
        destinations = [f"N{i}" for i in range(2, min(node_count, 22), 4)]
        rows.append({"component": "Nearest Neighbor route", "input_size": len(destinations),
                     "average_seconds": _timed(lambda g=graph, ds=destinations: plan_route(g, "N0", ds),
                                                repeats=3)})

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    csv_path, chart_path = output / "runtime_results.csv", output / "runtime_chart.png"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=("component", "input_size", "average_seconds"))
        writer.writeheader()
        writer.writerows(rows)
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Install dependencies with 'python -m pip install -r requirements.txt' to create the chart.") from exc
    components = list(dict.fromkeys(str(row["component"]) for row in rows))
    fig, axis = plt.subplots(figsize=(9, 5))
    for component in components:
        component_rows = [row for row in rows if row["component"] == component]
        axis.plot([row["input_size"] for row in component_rows],
                  [row["average_seconds"] for row in component_rows], marker="o", label=component)
    axis.set(xlabel="Input size (parcels, graph nodes, or delivery stops)", ylabel="Average runtime (seconds)",
             title="Mini Courier Planner Runtime")
    axis.grid(True, alpha=0.3)
    axis.legend()
    fig.tight_layout()
    fig.savefig(chart_path, dpi=160)
    plt.close(fig)
    return csv_path, chart_path
