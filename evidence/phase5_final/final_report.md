# Mini Courier Planner

## Objective

This project is a Python prototype for planning a courier trip. It sorts parcels by urgency, selects a high-value load within vehicle capacity, finds shortest road paths, and produces an approximate route that visits the selected customers and returns to the warehouse.

## Data and assumptions

The sample input has 60 parcel records and 20 customer destinations. Parcel rows provide an ID, destination, weight in grams, priority (1 is highest), deadline in days, and a value score. The road graph has 20 customer locations, a warehouse, and 34 undirected connections with positive integer distances in kilometers. The planner assumes one trip starts and ends at the warehouse. Multiple parcels for the same customer require one stop.

The parcel `value` is a sample benefit score for the knapsack objective. A real system would define this score from business rules such as revenue, urgency, or penalties for late delivery.

## Algorithms

**Merge Sort** orders parcels by earliest deadline, then priority number, then ID. Its time complexity is `O(n log n)` and its auxiliary space is `O(n)`.

**0/1 Knapsack dynamic programming** chooses a subset of indivisible parcels maximizing total value without exceeding the vehicle capacity. With `n` parcels and integer capacity `W`, time and space are `O(nW)`.

**Dijkstra's algorithm** uses an adjacency list and a min-heap to find shortest paths on nonnegative road distances. Its time complexity is `O((V + E) log V)`.

**Nearest-neighbor TSP approximation** repeatedly visits the closest unvisited destination using shortest-path distance, then returns to the warehouse. It is a heuristic and does not guarantee the globally shortest tour. Dijkstra supplies the shortest road path for every route leg.

## Demonstration results

For the supplied dataset and vehicle capacity of 10,000 g, knapsack selected 11 parcels totaling 9,914 g and value 967. The route visited Customer_01, Customer_02, Customer_07, Customer_06, Customer_11, Customer_12, Customer_13, Customer_14, Customer_15, Customer_20, Customer_19, Customer_18, Customer_17, and Customer_16, then returned to the warehouse. The calculated distance was 78 km.

One Dijkstra example from the warehouse to Customer_18 is `Warehouse → Customer_16 → Customer_17 → Customer_18`, with distance 14 km.

## Performance

The benchmark averages repeated runs on generated input sizes. The included CSV and chart contain the measured data. In this environment, Merge Sort took about 0.110 ms for 20 parcels and 0.472 ms for 200 parcels. Knapsack at capacity 5,000 took about 13.872 ms and 205.706 ms over the same parcel sizes. Dijkstra took about 0.042 ms for 20 nodes and 0.245 ms for 200 nodes. The route benchmark used five stops and graphs of increasing size, taking about 0.385 ms at 20 nodes and 3.540 ms at 200 nodes.

These values depend on hardware and Python environment. The linear chart places fast algorithms near zero when shown alongside knapsack; consult the CSV or compare components on separate scales. Parcel count, graph nodes, and delivery stops are different input units.

## Limitations and possible improvements

- Nearest neighbor is approximate and may produce a longer tour than an exact TSP solution.
- Knapsack's capacity is measured in integer grams, so runtime and memory use can grow with very large capacities.
- Parcel value scores are illustrative and should be based on a documented policy.
- Future work could use a sparse DP strategy, add more realistic map data, and compare route heuristics.

## Run instructions

Install the dependency and start the CLI from the project root:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Choose option 1 to generate a plan or option 2 to regenerate runtime data and the chart. Source code is in `src/`; input data is in `data/`.
