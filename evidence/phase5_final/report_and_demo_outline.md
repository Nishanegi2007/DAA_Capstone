# Phase 5 — Final Report and Demonstration Outline

Use this as the structure for the final report. Add your own screenshots from your computer and update results if you change the sample data or capacity.

1. **Title and objective:** Mini Courier Planner, course details, and the problem being solved.
2. **System design:** parcel and road data, assumptions, and workflow (see Phase 1 evidence).
3. **Algorithm implementation:** Merge Sort, 0/1 Knapsack, Dijkstra, nearest-neighbor TSP; explain each and state time/space complexity.
4. **Results:** show the 10,000 g sample packing and 72 km route, plus the hand-worked DP and Dijkstra examples.
5. **Performance:** insert the generated chart and discuss each algorithm separately. Explain the input sizes and runtime limits.
6. **Limitations and improvements:** nearest neighbor is approximate; knapsack runtime depends on numeric capacity; sample parcel value is a chosen score.
7. **How to run:** `python -m pip install -r requirements.txt`, then `python main.py`.
8. **Conclusion and submission link:** summarize what works and add your repository URL if applicable.

## Demo sequence

1. Show `data/parcels.csv` and `data/roads.csv`.
2. Run `python main.py`, choose option 1, and use capacity `10000`.
3. Explain one merge-sort comparison and trace one knapsack decision.
4. Trace the Warehouse-to-Customer_18 shortest path.
5. Explain how nearest neighbor chooses the next stop and why the result is approximate.
6. Choose option 2 and discuss the runtime chart and CSV.

Capture screenshots of the terminal output and chart, and place them in this folder before submission.
