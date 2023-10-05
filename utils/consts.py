from typing import Any
import pytz

url_authenticate = "https://api.sporteasy.net/v2.1/account/authenticate/"
url_list_teams = "https://api.sporteasy.net/v2.1/me/teams/"
url_list_seasons = "https://api.sporteasy.net/v2.1/teams/{team_id}/seasons/"
url_list_events = "https://api.sporteasy.net/v2.1/teams/{team_id}/events/"

PLAYED_WORDS = "played", "present", "available"
EVENT_TYPE = dict[str, int | str | Any | list[Any] | dict[str, Any]]
TIMEZONE = pytz.timezone("UTC")

ORDER_PRESENT = {
    "available": 50,
    "played": 51,
    "present": 52,
    "rsvp": 40,
    "not_selected": 30,
    "unavailable": 10,
    "not_played": 11,
}

MY_PRESENCE = {
    "available": "CONFIRMED",
    "played": "CONFIRMED",
    "present": "CONFIRMED",
    "rsvp": "NEEDS-ACTION",
    "not_selected": "CANCELLED",
    "unavailable": "CANCELLED",
    "not_played": "CANCELLED",
}
