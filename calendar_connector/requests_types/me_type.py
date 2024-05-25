from typing import TypedDict, Any, Optional

from calendar_connector.requests_types.shared_type import AvatarType


class LinkType(TypedDict):
    method: str
    url: str


class MeType(TypedDict):
    activated_at: str
    analytics_id: str
    avatar: AvatarType
    date_of_birth: Optional[str]
    default_language: str
    email: str
    email_verification_deferment: bool
    first_name: str
    full_name: str
    gender: Optional[str]
    height: Optional[int]
    id: int
    is_verified: bool
    last_name: str
    phone_number: Optional[str]
    profile_display_good_deals: bool
    profile_display_origin_survey: bool
    profile_display_purpose_survey: bool
    weight: Optional[int]
    _links: dict[str, LinkType]
