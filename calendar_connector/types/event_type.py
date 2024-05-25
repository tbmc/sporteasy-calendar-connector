from typing import TypedDict, Any, Optional

from calendar_connector.types.season_type import SeasonType
from calendar_connector.types.shared_type import CountryType


class LocationType(TypedDict):
    id: int
    is_stadium: bool
    lat: float
    lng: float
    name: str
    url: str
    formatted_address: str
    country: CountryType


class GroupType(TypedDict):
    attendance_status: str
    importance_level: int
    localized_name: str
    slug_name: str
    target_groups: list[str]


class OpponentType(TypedDict):
    id: str
    full_name: str
    is_current_team: bool
    is_home: bool
    jersey_color: Optional[Any]
    match_outcome: str
    score: int
    short_name: str


class AttendanceGroupType(TypedDict):
    attendance_status: str
    count: int
    importance_level: int
    localized_name: str
    slug_name: str


class CategoryType(TypedDict):
    championship_day: int
    id: int
    localized_name: str
    slug_name: str
    type: str


class RegistrationParametersType(TypedDict):
    hide_attendance: bool


class MeType(TypedDict):
    group: GroupType
    opponent: str
    url: str


class EventType(TypedDict):
    id: int
    name: str
    start_at: str
    end_at: str
    url: str
    thread_id: int
    location: LocationType
    available_threshold_reached: bool
    can_see_attendance: bool
    is_cancelled: bool
    is_date_unknown: bool
    is_past: bool
    is_recurring: bool
    is_sportive: bool
    me: MeType
    opponent_left: Optional[OpponentType]
    opponent_right: Optional[OpponentType]
    registration_open_at: str
    step: str
    attendance_groups: list[AttendanceGroupType]
    category: CategoryType
    registration_parameters: RegistrationParametersType
    season: SeasonType
