from typing import Any
import pytz

url_base = "https://api.sporteasy.net/v2.1"
url_authenticate = f"{url_base}/account/authenticate/"
url_csrf = f"{url_base}/account/csrf/"
url_me = f"{url_base}/me/"
url_list_teams = f"{url_base}/me/teams/"

url_team_id_base = url_base + "/teams/{team_id}"
url_list_seasons = f"{url_team_id_base}/seasons/"
url_list_events = f"{url_team_id_base}/events/"

url_event_base = url_team_id_base + "/events/{event_id}"
url_put_event_presence = url_event_base + "/profiles/{profile_id}/"

route_change_presence = "/api/change_my_presence"

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
