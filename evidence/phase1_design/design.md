# Phase 1 — Courier Problem Design

## Problem

Mini Courier Planner selects parcels that fit a delivery vehicle and plans a route from the warehouse to the selected customers and back. The sample dataset contains 60 parcels, 20 customer locations, and an undirected road network with 34 connections.

## Parcel data

| Field | Meaning |
|---|---|
| `id` | Unique parcel identifier |
| `destination` | Customer location |
| `weight_g` | Parcel weight in whole grams |
| `priority` | 1 is highest urgency; 3 is lowest |
| `deadline_days` | Days remaining until delivery deadline |
| `value` | Benefit score used by the knapsack objective |

Road records contain `start`, `end`, and `distance_km`. Roads are treated as undirected and distances are positive whole kilometers.

## Algorithms selected

- **Merge Sort:** orders by earliest deadline, then priority number, then parcel ID. Time: `O(n log n)`.
- **0/1 Knapsack dynamic programming:** maximizes total parcel value subject to the vehicle capacity. Time and space: `O(nW)`, where `n` is parcel count and `W` is capacity in grams.
- **Dijkstra with a min-heap:** finds shortest road paths for nonnegative distances. Time: `O((V + E) log V)` for the adjacency-list graph.
- **Nearest-neighbor TSP approximation:** repeatedly visits the closest unvisited customer according to Dijkstra distances, then returns to the warehouse. Route optimization is approximate and may not find the globally shortest tour.

## Workflow

CSV parcel and road data → Merge Sort parcel list → Knapsack load selection → Dijkstra shortest path distances → nearest-neighbor stop order → expanded road route and total distance → performance results.

## Design assumptions

The van starts and ends at `Warehouse`. The sample value is an explicit demonstration score; for a real use case, document how urgency or revenue maps to value. Multiple parcels going to the same customer require only one route stop.
