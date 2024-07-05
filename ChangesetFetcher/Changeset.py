from datetime import datetime

from dataclasses import dataclass
from typing import Optional


@dataclass
class Changeset:
    """
    A OSM Changeset (https://wiki.openstreetmap.org/wiki/Changeset).
    """
    id: int
    created_at: datetime
    closed_at: Optional[datetime]  # Is null if changeset is still open
    open: bool
    user: str
    uid: int
    min_lat: Optional[float]
    max_lat: Optional[float]
    min_lon: Optional[float]
    max_lon: Optional[float]
    comments_count: int
    num_changes: int
