# Mini Courier Planner

A Python command-line project for a Design and Analysis of Algorithms capstone. It sorts parcels, selects a load with 0/1 knapsack dynamic programming, finds road shortest paths with Dijkstra, plans a multi-stop route with nearest neighbor, and records runtime measurements.

## Requirements

- Python 3.10 or newer
- Matplotlib for runtime chart generation

## Run

From this project folder:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Choose **1** to generate a delivery plan, then enter a vehicle capacity in grams (default `10000`). Choose **2** to create runtime evidence under `results/`. Choose **3** to draw the connected road network and highlight the selected route for a `10000` g load in `evidence/phase3_routes/road_network_10000g.png`.

## Data files

`data/parcels.csv` contains 60 parcels across 20 customers. Its columns are `id`, `destination`, `weight_g`, `priority`, `deadline_days`, `value`. Priority 1 is most urgent. Weight is an integer number of grams; value is the benefit used by knapsack.

`data/roads.csv` contains a connected 20-customer road grid plus three warehouse connections. Its columns are `start`, `end`, `distance_km`. Roads are treated as undirected and distances must be positive whole kilometers.

## Algorithms and complexity

- Merge Sort: orders by earliest deadline, then priority, then parcel ID; `O(n log n)` time.
- 0/1 Knapsack: maximizes total value subject to vehicle capacity; `O(nW)` time and space, where `W` is capacity in grams.
- Dijkstra with a binary heap: shortest road distances; `O((V + E) log V)` for the adjacency-list representation.
- Nearest neighbor: chooses the next closest unvisited destination using Dijkstra distances, then returns to the warehouse. The route choice is an approximation to TSP; each individual leg is a shortest road path.

## Project layout

```text
main.py
src/              algorithm and data modules
data/             sample parcel and road CSV files
results/          generated runtime CSV and chart
screenshots/       place demonstration screenshots here
requirements.txt
```

The parcel benefit values are sample assumptions for demonstrating knapsack. Explain your chosen value policy in the report. The nearest-neighbor order is not guaranteed to be the globally shortest tour.
