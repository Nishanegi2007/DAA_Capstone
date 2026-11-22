# Capstone Evidence Checklist

Save your evidence in the matching phase folder. Use screenshots, diagrams, tables, or short explanations that show your own work. Keep a copy of the final report and demo evidence in `phase5_final/`.

## Phase 1 — Courier problem design

In `phase1_design/`, add:

- A one-page explanation of the problem and how your planner solves it.
- A parcel data dictionary explaining ID, destination, weight, priority, deadline, and value. The supplied sample has 60 parcels across 20 customers.
- A road network diagram or readable graph listing. The supplied road data is in `data/roads.csv`.
- A workflow diagram: CSV input → Merge Sort → Knapsack → Dijkstra → Nearest Neighbor → output.
- A short reason for choosing each algorithm, plus its expected time complexity.

## Phase 2 — Parcel prioritization and packing

In `phase2_parcels/`, add:

- A screenshot or copied output showing parcels sorted by deadline, then priority.
- The vehicle capacity you used and the selected parcel IDs.
- Total selected weight and value. Confirm the selected weight does not exceed capacity.
- A small hand-worked knapsack DP table, or a screenshot of a table for a small sample. The full 60-parcel result can be shown as program output.
- A short note that sorting ranks parcels, while knapsack chooses the best-value combination that fits.

## Phase 3 — Graph and route planning

In `phase3_routes/`, add:

- The graph diagram or a clear listing of roads and distances.
- One Dijkstra example: start, destination, shortest path, and distance. Show enough steps to trace how the answer was obtained.
- The nearest-neighbor delivery stop order and the expanded road-by-road route from the program.
- The total distance, including the return to the warehouse. Explain that nearest neighbor is an approximation and may not find the globally shortest tour.

## Phase 4 — Performance

In `phase4_performance/`, add:

- The runtime chart and `results/runtime_results.csv` produced by menu option 2.
- A short description of the hardware/software environment and how many repeated timings were averaged (the benchmark code averages several runs).
- A short interpretation of the trend for each algorithm. Explain why very small runtimes may look flat on a shared chart scale.
- Keep input units clear: parcel count, graph nodes, or delivery stops. Avoid comparing raw times as if the components used the same input size.

## Phase 5 — Final report and demonstration

In `phase5_final/`, add:

- Your final report, including design choices, algorithm explanations, results, and limitations.
- Screenshots of the application running and the final delivery plan.
- Clear setup and execution instructions. From the project folder, use `python -m pip install -r requirements.txt` and `python main.py`.
- Your GitHub repository link, if submitting through GitHub, or confirmation that the project files are ready for upload.
- A short demo outline: load data, generate a plan, explain one algorithm step, and show the runtime evidence.

## Before submitting

- Make sure screenshots are readable and show enough of the terminal or chart to identify what they demonstrate.
- Use consistent sample inputs and settings in your explanations.
- Be ready to explain the logic and complexity of every algorithm, and to run it on a changed or unseen input during the viva.
