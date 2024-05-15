from icalendar import Calendar, vText

from calendar_connector.datetime_utils import (
    get_current_datetime,
)
from calendar_connector.env import load_env_data
from calendar_connector.event_convertor import event_to_calendar_event
from calendar_connector.sporteasy_connector import SporteasyConnector




class CalendarConverter:
    def __init__(self) -> None:
        self.connector = SporteasyConnector()

    def get_calendar_text(
        self, username: str, password: str, team_id: str | None = None
    ) -> str:
        self.connector.login(username, password)
        teams = self.connector.list_teams()

        cal = Calendar()
        cal.add("summary", vText("SportEasyCalendar"))
        cal.add("prodid", "-//Sporteasy Calendar Connector")
        cal.add("version", "2.0")
        cal.add("vtimezone", "UTC")
        cal.add("calscale", "GREGORIAN")
        cal.add("method", "PUBLISH")
        cal.add("x-wr-calname", "SportEasy Calendar")
        cal.add("x-wr-timezone", "Europe/Paris")

        formatted_time = get_current_datetime().strftime("%Y-%m-%d %H:%M:%S")
        cal.add("x-wr-caldesc", f"SportEasy Calendar | Last sync: {formatted_time}")
        cal.add("REFRESH-INTERVAL;VALUE=DURATION", "PT8H")
        cal.add("X-PUBLISHED-TTL", "PT8H")

        for current_team_id, team_name in teams:
            # Ignore other teams
            if (
                team_id is not None
                and team_id != ""
                and int(team_id) != current_team_id
            ):
                continue
            events = self.connector.list_events(current_team_id)
            for event in events:
                cal.add_component(event_to_calendar_event(team_name, event))

        text_calendar: str = cal.to_ical().decode("utf-8").strip()

        return text_calendar


def main() -> None:
    username, password, team_id = load_env_data()

    calendar_converter = CalendarConverter()
    calendar_content = calendar_converter.get_calendar_text(username, password, team_id)
    with open("./test.ics", "w", encoding="utf-8") as f:
        f.write(calendar_content)


if __name__ == "__main__":
    main()
