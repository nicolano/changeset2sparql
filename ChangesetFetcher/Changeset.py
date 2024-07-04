from dataclasses import dataclass


@dataclass
class Changeset:
    """
    A OSM Changeset (https://wiki.openstreetmap.org/wiki/Changeset).
    """
    id: int
    created_at: str
    closed_at: str
    user: str
    user_id: int
    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float
    comments_count: int
    changes_count: int
