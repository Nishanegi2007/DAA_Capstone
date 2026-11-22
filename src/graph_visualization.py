"""Draw the courier road graph as a labeled network diagram."""

from pathlib import Path

from .models import Road


def save_road_network(roads: list[Road], output_path: str | Path,
                      route: list[str] | None = None,
                      title: str = "Mini Courier Planner — Road Network") -> Path:
    """Save a labeled road graph; optionally highlight an expanded delivery route."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Install dependencies with 'python -m pip install -r requirements.txt' to draw the graph.") from exc

    positions: dict[str, tuple[float, float]] = {"Warehouse": (-2.3, 1.5)}
    for number in range(1, 21):
        row, column = divmod(number - 1, 5)
        positions[f"Customer_{number:02d}"] = (float(column), float(3 - row))

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    route_edges = {
        frozenset((start, end)) for start, end in zip(route or [], (route or [])[1:])
    }
    route_nodes = set(route or [])
    fig, axis = plt.subplots(figsize=(13, 8))
    axis.set_title(title, fontsize=17, pad=18)

    for start, end, distance in roads:
        x1, y1 = positions[start]
        x2, y2 = positions[end]
        on_route = frozenset((start, end)) in route_edges
        color = "#d32f2f" if on_route else "#78909c"
        width = 3.5 if on_route else 1.8
        if {start, end} == {"Warehouse", "Customer_05"}:
            # Route this long connector above the grid so it does not cross a node.
            t_values = [step / 50 for step in range(51)]
            control_x, control_y = 0.4, 4.2
            xs = [(1-t)**2*x1 + 2*(1-t)*t*control_x + t**2*x2 for t in t_values]
            ys = [(1-t)**2*y1 + 2*(1-t)*t*control_y + t**2*y2 for t in t_values]
            axis.plot(xs, ys, color=color, linewidth=width, zorder=1)
            mx, my = (xs[25], ys[25])
        else:
            axis.plot((x1, x2), (y1, y2), color=color, linewidth=width, zorder=1)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        axis.text(mx, my, str(distance), fontsize=8, ha="center", va="center",
                  color="#263238", bbox={"boxstyle": "round,pad=0.15", "facecolor": "white",
                                        "edgecolor": "none", "alpha": 0.9}, zorder=2)

    for node, (x, y) in positions.items():
        is_warehouse = node == "Warehouse"
        axis.scatter(x, y, s=1000 if is_warehouse else 680,
                     color="#d32f2f" if is_warehouse or node in route_nodes else "#1976d2",
                     edgecolors="white", linewidths=1.5, zorder=3)
        label = "WH" if is_warehouse else node.replace("Customer_", "C")
        axis.text(x, y, label, color="white", fontsize=8,
                  fontweight="bold", ha="center", va="center", zorder=4)
        if is_warehouse:
            axis.text(x, y - 0.4, "Warehouse", color="#9a4300", fontsize=9,
                      fontweight="bold", ha="center", va="top", zorder=4)

    axis.set_aspect("equal")
    axis.set_xlim(-3.3, 4.7)
    axis.set_ylim(-0.7, 3.8)
    axis.axis("off")
    axis.text(0.5, -0.08, "Edge labels show road distance in kilometers; roads are undirected.",
              transform=axis.transAxes, ha="center", fontsize=10, color="#455a64")
    if route:
        axis.text(0.5, -0.12, "Red edges and nodes show the selected delivery route.",
                  transform=axis.transAxes, ha="center", fontsize=10, color="#b71c1c")
    fig.tight_layout()
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output
