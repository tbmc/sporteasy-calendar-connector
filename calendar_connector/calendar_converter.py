from typing import Optional, cast
import logging

from icalendar import Calendar, vText

from calendar_connector.database.user import save_user
from calendar_connector.datetime_utils import (
    get_formatted_current_time,
)
from calendar_connector.env import load_env_data
from calendar_connector.event_convertor import event_to_calendar_event
from calendar_connector.event_utils.description import GenerateLinksData
from calendar_connector.sporteasy_connector import SporteasyConnector

logger = logging.getLogger(__name__)


class CalendarConverter:
    def __init__(self) -> None:
        self.connector = SporteasyConnector()

    def get_calendar_text(
        self,
        username: str,
        password: str,
        save_login: bool,
        url_root: str,
        team_id: Optional[str] = None,
    ) -> str:
        """
        Retrieves the calendar text from SportEasy for the specified team.

        Args:
            username (str): The username for the SportEasy account.
            password (str): The password for the SportEasy account.
            save_login (bool): If True, save the login credentials.
            url_root (str): The base URL for the SportEasy API.
            team_id (Optional[str], optional): The ID of the team to retrieve events for. Defaults to None.

        Returns:
            str: The calendar text in iCalendar format.

        Raises:
            Exception: If an error occurs while retrieving the calendar text.

        Example:
            ```python
            calendar_converter = CalendarConverter()
            calendar_content = calendar_converter.get_calendar_text(
                "example_username", "example_password", False, "http://localhost:5000/", "12345"
            )
            ```
        """
        logger.info("Starting calendar generation (team_id_filter=%s)", team_id)
        self.connector.login(username, password)

        links_data: Optional[GenerateLinksData] = None
        if save_login:
            logger.debug("Saving user credentials for presence links")
            user = save_user(username, password)
            links_data = GenerateLinksData(
                cast(int, user.id),
                username,
                password,
                cast(str, user.salt),
                url_root,
            )
        else:
            logger.debug("Skipping credential persistence (save_login disabled)")

        teams = self.connector.list_teams()
        logger.info("Retrieved %s teams", len(teams))

        cal = Calendar()
        cal.add("summary", vText("SportEasyCalendar"))
        cal.add("prodid", "-//Sporteasy Calendar Connector")
        cal.add("version", "2.0")
        cal.add("vtimezone", "UTC")
        cal.add("calscale", "GREGORIAN")
        cal.add("method", "PUBLISH")
        cal.add("x-wr-calname", "SportEasy Calendar")
        cal.add("x-wr-timezone", "Europe/Paris")

        cal.add(
            "x-wr-caldesc",
            f"SportEasy Calendar | Last sync: {get_formatted_current_time()}",
        )
        cal.add("REFRESH-INTERVAL;VALUE=DURATION", "PT8H")
        cal.add("X-PUBLISHED-TTL", "PT8H")

        total_events = 0
        for current_team_id, team_name, team_url in teams:
            # Ignore other teams
            if (
                team_id is not None
                and team_id != ""
                and int(team_id) != current_team_id
            ):
                logger.debug(
                    "Skipping team %s (%s) because it does not match filter %s",
                    current_team_id,
                    team_name,
                    team_id,
                )
                continue
            events = self.connector.list_events(current_team_id)
            logger.debug(
                "Retrieved %s events for team_id=%s team_name=%s",
                len(events),
                current_team_id,
                team_name,
            )
            for event in events:
                cal.add_component(
                    event_to_calendar_event(
                        current_team_id, team_name, event, links_data, team_url
                    )
                )
            total_events += len(events)

        text_calendar: str = cal.to_ical().decode("utf-8").strip()

        logger.info(
            "Calendar generation completed (teams=%s, events=%s)",
            len(teams),
            total_events,
        )

        return text_calendar


def main() -> None:
    username, password, team_id = load_env_data()

    calendar_converter = CalendarConverter()
    calendar_content = calendar_converter.get_calendar_text(
        username, password, False, "http://localhost:5000/", team_id
    )
    with open("./test.ics", "w", encoding="utf-8") as f:
        f.write(calendar_content)


if __name__ == "__main__":
    main()
