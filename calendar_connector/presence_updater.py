from calendar_connector.sporteasy_connector import SporteasyConnector
from calendar_connector.database.user import get_username_password


def set_presence_to_event(
    team_id: int, event_id: int, user_id: int, presence: bool
) -> None:
    username, password = get_username_password(user_id)
    connector = SporteasyConnector()
    connector.login(username, password)

    connector.put_presence_status(team_id, event_id, presence)
