"""Command-line entry point for the Mini Courier Planner."""

from pathlib import Path

from src.data_loader import load_parcels, load_roads
from src.graph import build_graph
from src.graph_visualization import save_road_network
from src.knapsack import choose_parcels
from src.performance import run_benchmarks
from src.routing import plan_route
from src.sorting import merge_sort_parcels


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


def print_plan(capacity: int = 10000) -> None:
    parcels = load_parcels(DATA_DIR / "parcels.csv")
    roads = load_roads(DATA_DIR / "roads.csv")
    graph = build_graph(roads)

    ordered = merge_sort_parcels(parcels)
    selected, total_weight, total_value = choose_parcels(ordered, capacity)
    route, distance = plan_route(graph, "Warehouse", [p["destination"] for p in selected])

    print("\nParcels ordered by deadline, then priority:")
    for parcel in ordered:
        print(f"  {parcel['id']}: {parcel['destination']}, {parcel['weight']} g, "
              f"priority {parcel['priority']}, deadline day {parcel['deadline_days']}")
    print(f"\nVehicle capacity: {capacity:,} g")
    print("Selected parcels:")
    for parcel in selected:
        print(f"  {parcel['id']}: {parcel['destination']} ({parcel['weight']:,} g; "
              f"value {parcel['value']})")
    print(f"Total load: {total_weight:,} g | Total value: {total_value}")
    print("\nRoute: " + " -> ".join(route))
    print(f"Route distance: {distance:,} km")


def main() -> None:
    while True:
        print("\n=== MINI COURIER PLANNER ===")
        print("1. Generate delivery plan")
        print("2. Run performance benchmarks")
        print("3. Save 10,000 g delivery route diagram")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            raw = input("Vehicle capacity in grams [10000]: ").strip()
            try:
                capacity = int(raw) if raw else 10000
                if capacity <= 0:
                    raise ValueError
                print_plan(capacity)
            except ValueError:
                print("Capacity must be a positive whole number of grams.")
            except (OSError, ValueError) as exc:
                print(f"Could not create plan: {exc}")
        elif choice == "2":
            try:
                csv_path, chart_path = run_benchmarks(ROOT / "results")
                print(f"Runtime data saved to {csv_path}")
                print(f"Runtime chart saved to {chart_path}")
            except (OSError, RuntimeError) as exc:
                print(f"Could not run benchmarks: {exc}")
        elif choice == "3":
            try:
                parcels = load_parcels(DATA_DIR / "parcels.csv")
                roads = load_roads(DATA_DIR / "roads.csv")
                graph = build_graph(roads)
                selected, total_weight, total_value = choose_parcels(parcels, 10000)
                route, distance = plan_route(graph, "Warehouse", [p["destination"] for p in selected])
                diagram = save_road_network(
                    roads,
                    ROOT / "evidence" / "phase3_routes" / "road_network_10000g.png",
                    route,
                    "Courier Road Network — 10,000 g Delivery Plan",
                )
                print(f"10,000 g route diagram saved to {diagram}")
                print(f"Selected load: {total_weight:,} g | Value: {total_value} | Distance: {distance} km")
            except (OSError, RuntimeError, KeyError) as exc:
                print(f"Could not draw road network: {exc}")
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
