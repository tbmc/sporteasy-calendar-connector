from icalendar import Event

from calendar_connector.consts import MY_PRESENCE
from calendar_connector.custom_exceptions import AttributeNotFoundException
from calendar_connector.normalize import normalize
from calendar_connector.requests_types.event_type import EventType


def _status_to_ics_status(sp_status: str) -> str:
    sp_status = sp_status.upper()
    if sp_status == "CONFIRMED":
        return "CONFIRMED"
    if sp_status == "CANCELLED":
        return "CANCELLED"
    if sp_status == "NEEDS-ACTION":
        return "TENTATIVE"
    return sp_status


def extract_event_summary(event_data: EventType, event: Event, team_name: str) -> None:
    name = normalize(event_data["name"])
    if team_name not in name:
        summary = f"{team_name} - {name}"
    else:
        summary = name
    if "is_cancelled" in event_data and event_data["is_cancelled"]:
        summary = f"CANCELLED | {summary}"

    # opponent_right = cast(dict[str, int | str | None] | None, event_data["opponent_right"])
    # opponent_left = cast(dict[str, int | str | None] | None, event_data["opponent_left"])
    # if opponent_left is not None and opponent_right is not None:
    #     if opponent_left["id"] == team_id:
    #         opponent_name = opponent_right["short_name"]
    #     else:
    #         opponent_name = opponent_left["short_name"]
    #     summary += f" - contre {opponent_name}"

    me_object = event_data.get("me", {})
    if me_object is not None and me_object.get("group") is not None:
        group = me_object.get("group", {})
        localized_name_presence = group.get("localized_name")
        if localized_name_presence is not None:
            summary += f" - {normalize(localized_name_presence)}"

        slug_presence = group.get("slug_name")
        if slug_presence is None:
            raise AttributeNotFoundException("slug_name")
        presence = MY_PRESENCE.get(slug_presence)
        if presence is None:
            raise AttributeNotFoundException("slug_presence")
        event.add("status", _status_to_ics_status(presence))

    event.add("summary", summary)
