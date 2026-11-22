# Phase 3 — Graph and Route Planning

## Graph representation

The graph is an adjacency list built from `data/roads.csv`. Each road is bidirectional and stores its distance in kilometers. The sample graph has 20 customer nodes plus the warehouse, with 34 road connections.

The connected-node diagram is `road_network.png`. The 10,000 g trip diagram is `road_network_10000g.png`; it highlights the selected route in red. Generate or refresh the trip diagram from the app by choosing menu option 3.

## Dijkstra example

For a path from `Warehouse` to `Customer_18`, Dijkstra returns:

`Warehouse → Customer_16 → Customer_17 → Customer_18`

Total shortest-path distance: **14 km**. The three road segments are 7 km, 2 km, and 5 km respectively.

## Integrated delivery route

Using all parcels selected at 10,000 g capacity, the planner visits each selected destination once and returns to the warehouse:

`Warehouse → Customer_01 → Customer_02 → Customer_07 → Customer_06 → Customer_11 → Customer_12 → Customer_13 → Customer_14 → Customer_15 → Customer_20 → Customer_19 → Customer_18 → Customer_17 → Customer_16 → Warehouse`

Total distance: **78 km**. The warehouse-to-Customer_02 shortest leg passes through Customer_01, which is also one of the selected delivery locations. Each segment in the expanded route follows a shortest road path. The stop order uses nearest neighbor, so the overall tour is an approximation and is not guaranteed to be globally shortest.
