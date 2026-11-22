"""Merge Sort for parcel deadline and priority ordering."""

from .models import Parcel


def _key(parcel: Parcel) -> tuple[int, int, str]:
    # Earlier deadline first; smaller priority number means more urgent.
    return parcel["deadline_days"], parcel["priority"], parcel["id"]


def merge_sort_parcels(parcels: list[Parcel]) -> list[Parcel]:
    """Return a sorted copy in O(n log n) time."""
    if len(parcels) <= 1:
        return parcels.copy()
    middle = len(parcels) // 2
    left = merge_sort_parcels(parcels[:middle])
    right = merge_sort_parcels(parcels[middle:])
    merged: list[Parcel] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if _key(left[i]) <= _key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    return merged + left[i:] + right[j:]
