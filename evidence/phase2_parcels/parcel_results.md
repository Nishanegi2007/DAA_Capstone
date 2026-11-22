# Phase 2 — Parcel Prioritization and Packing

## Sorting evidence

The program sorts by deadline ascending, then priority ascending (1 is most urgent), then parcel ID. With the current 60-parcel CSV, the first twelve results are:

| Parcel | Deadline (days) | Priority |
|---|---:|---:|
| P004 | 1 | 1 |
| P010 | 1 | 1 |
| P016 | 1 | 1 |
| P022 | 1 | 1 |
| P028 | 1 | 1 |
| P034 | 1 | 1 |
| P040 | 1 | 1 |
| P046 | 1 | 1 |
| P052 | 1 | 1 |
| P058 | 1 | 1 |
| P002 | 1 | 2 |
| P008 | 1 | 2 |

## Current dataset packing result

At a capacity of **10,000 g**, 0/1 Knapsack selects **11 parcels**, with total weight **9,914 g** and total value **967**. The selected IDs are P040, P052, P002, P014, P026, P042, P013, P041, P053, P015, and P039. This is within the capacity. The objective is to maximize the sum of the `value` field.

## Small hand-worked DP example

This compact example makes the dynamic programming calculation easy to trace. Capacity is 5 kg.

| Parcel | Weight (kg) | Value |
|---|---:|---:|
| A | 2 | 30 |
| B | 3 | 50 |
| C | 4 | 60 |

Each table cell is the best value using the parcels processed so far and that capacity:

| Parcels processed \ capacity (kg) | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| None | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 30 | 30 | 30 | 30 |
| A, B | 0 | 0 | 30 | 50 | 50 | 80 |
| A, B, C | 0 | 0 | 30 | 50 | 60 | 80 |

The optimal choice is A + B: 5 kg total and value 80. The input is sorted for prioritization, while knapsack chooses a value-maximizing combination; it does not simply take the first parcels in the sorted list.
