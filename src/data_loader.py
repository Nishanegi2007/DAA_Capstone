"""CSV loading and input validation."""

import csv
from pathlib import Path

from .models import Parcel, Road


def load_parcels(path: str | Path) -> list[Parcel]:
    parcels: list[Parcel] = []
    with Path(path).open("r", newline="", encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            parcel: Parcel = {
                "id": row["id"].strip(),
                "destination": row["destination"].strip(),
                "weight": int(row["weight_g"]),
                "priority": int(row["priority"]),
                "deadline_days": int(row["deadline_days"]),
                "value": int(row["value"]),
            }
            if (not parcel["id"] or not parcel["destination"] or parcel["weight"] <= 0
                    or parcel["priority"] not in (1, 2, 3) or parcel["deadline_days"] < 0
                    or parcel["value"] < 0):
                raise ValueError(f"Invalid parcel record: {row}")
            parcels.append(parcel)
    if not parcels:
        raise ValueError("Parcel CSV contains no parcel records.")
    return parcels


def load_roads(path: str | Path) -> list[Road]:
    roads: list[Road] = []
    with Path(path).open("r", newline="", encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            start, end, distance = row["start"].strip(), row["end"].strip(), int(row["distance_km"])
            if not start or not end or start == end or distance <= 0:
                raise ValueError(f"Invalid road record: {row}")
            roads.append((start, end, distance))
    if not roads:
        raise ValueError("Road CSV contains no road records.")
    return roads
