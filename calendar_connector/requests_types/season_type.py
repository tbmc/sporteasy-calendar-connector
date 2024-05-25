from typing import TypedDict


class SeasonType(TypedDict):
    archived: bool
    current: bool
    start_date: str
    end_date: str
    name: str
    slug_name: str
