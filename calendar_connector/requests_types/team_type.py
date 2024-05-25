from typing import TypedDict, Any, Optional

from calendar_connector.requests_types.shared_type import (
    CountryType,
    LogoType,
    SiteType,
    CoverType,
    AvatarType,
)


class AgeCategoryType(TypedDict):
    age_range: str
    is_youth: bool
    localized_age_range: str


class RoleType(TypedDict):
    slug_name: str
    localized_name: str


class MemberRoleType(TypedDict):
    count: int
    role: RoleType


class SportType(TypedDict):
    slug_name: str
    localized_name: str
    icon_url: str
    is_generic: bool


class FormatType(TypedDict):
    nb_players: int
    sport_slug_name: str
    localized_name: str


class ClubType(TypedDict):
    id: int
    name: str
    url: str


class DefaultStadiumType(TypedDict):
    id: int
    name: str
    formatted_address: str
    lat: float
    lng: float
    country: CountryType
    url: str
    is_stadium: bool


class ProfileType(TypedDict):
    id: int
    first_name: str
    last_name: str
    full_name: str
    avatar: AvatarType
    email: str
    phone_number: str
    activated_at: str
    date_of_birth: Optional[str]
    weight: Optional[Any]
    height: Optional[Any]
    default_language: str
    is_active: bool
    nickname: Optional[str]
    invited_at: Optional[str]


class MeType(TypedDict):
    is_admin: bool
    licence_number: str
    year_of_arrival: Optional[str]
    profile: ProfileType
    role: RoleType
    usual_tactic_position: Optional[Any]
    jersey_number: Optional[Any]
    is_unavailable: bool
    _links: dict


class PlanType(TypedDict):
    slug_name: str
    name: str
    max_number_of_member: Optional[Any]
    price: str
    has_advertising: bool
    is_premium: bool


class CurrentSubscriptionType(TypedDict):
    id: int
    plan: PlanType
    start_at: str
    end_at: str
    is_auto_renew: bool
    blocking_countdown: Optional[Any]
    members_count: Optional[Any]
    balance: Optional[Any]
    pending_balance: Optional[Any]
    next: Optional[Any]
    profile: Optional[Any]


class CurrentSeasonType(TypedDict):
    id: int
    name: str
    current: Optional[Any]


class MobilePlansType(TypedDict):
    ios: list[str]
    android: list[str]


class TeamType(TypedDict):
    age_category: AgeCategoryType
    age_range: str
    email: str
    full_name: str
    gender: str
    id: int
    is_impersonated: bool
    motto: str
    name: str
    practice_level: str
    short_name: str
    slug_name: str
    team_group_type: str
    timezone: str
    url: str
    url_categories: str
    url_events: str
    url_opponents: str
    url_seasons: str
    url_stadiums: str
    web_url: str

    location: Optional[Any]
    onboarding_info: Optional[Any]
    phone_number: Optional[Any]
    sponsor: Optional[Any]
    sponsor_information: Optional[Any]
    year_of_creation: Optional[Any]

    country: CountryType
    logo: LogoType
    site: SiteType
    member_roles: list[MemberRoleType]
    sport: SportType
    format: FormatType
    cover: CoverType
    club: ClubType
    default_stadium: DefaultStadiumType
    me: MeType
    current_subscription: CurrentSubscriptionType
    current_season: CurrentSeasonType
    mobile_plans: MobilePlansType
    managers: list[Any]
