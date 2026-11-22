"""0/1 knapsack using a bottom-up dynamic-programming table."""

from .models import Parcel


def choose_parcels(parcels: list[Parcel], capacity: int) -> tuple[list[Parcel], int, int]:
    """Maximize parcel value within capacity; return chosen records, weight, value.

    Weight and capacity use the same integer unit (grams in the supplied data).
    In a value tie, the earlier DP choice is retained for deterministic output.
    Complexity: O(number_of_parcels * capacity) time and space.
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, parcel in enumerate(parcels, start=1):
        weight, value = parcel["weight"], parcel["value"]
        for limit in range(capacity + 1):
            dp[i][limit] = dp[i - 1][limit]
            if weight <= limit:
                dp[i][limit] = max(dp[i][limit], value + dp[i - 1][limit - weight])

    selected: list[Parcel] = []
    remaining = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            remaining -= parcel["weight"]
    selected.reverse()
    return selected, sum(p["weight"] for p in selected), dp[n][capacity]
