import logging

from calendar_connector.sporteasy_connector import SporteasyConnector
from calendar_connector.database.user import get_username_password

logger = logging.getLogger(__name__)


def set_presence_to_event(
    team_id: int, event_id: int, user_id: int, presence: bool
) -> None:
    logger.debug(
        "Loading credentials to update presence (team_id=%s, event_id=%s, user_id=%s)",
        team_id,
        event_id,
        user_id,
    )
    username, password = get_username_password(user_id)
    connector = SporteasyConnector()
    connector.login(username, password)

    connector.put_presence_status(team_id, event_id, presence)
    logger.info(
        "Presence update request sent (team_id=%s, event_id=%s, user_id=%s, presence=%s)",
        team_id,
        event_id,
        user_id,
        presence,
    )
