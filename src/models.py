"""Shared record definitions used by the planner."""

from typing import TypedDict


class Parcel(TypedDict):
    id: str
    destination: str
    weight: int
    priority: int
    deadline_days: int
    value: int


Road = tuple[str, str, int]
