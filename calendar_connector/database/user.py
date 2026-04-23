import logging

from peewee import PrimaryKeyField, CharField

from calendar_connector.cryptography import generate_salt, generate_hash
from calendar_connector.custom_exceptions import TooManyUsersException
from calendar_connector.database.base_models import BaseModel

logger = logging.getLogger(__name__)


class User(BaseModel):
    id = PrimaryKeyField()
    username = CharField(unique=True, max_length=256, null=False)
    password = CharField(max_length=256, null=False)
    salt = CharField(max_length=51, null=False)


def save_user(username: str, password: str) -> User:
    already_existing_users: list[User] = list(User.select().where(User.username == username)) # pyright: ignore[reportUnknownMemberType]
    logger.debug("save_user called for username=%s (matches=%s)", username, len(already_existing_users))

    if len(already_existing_users) > 1:
        logger.error("Multiple users found for username=%s", username)
        raise TooManyUsersException(username, len(already_existing_users))

    if len(already_existing_users) == 0:
        user = User(username=username, password=password, salt=generate_salt())
        user.save() # pyright: ignore[reportUnknownMemberType]
        logger.info("Created new user record for username=%s", username)
        return user

    user = already_existing_users[0]
    if user.password != password:
        user.password = password # pyright: ignore[reportAttributeAccessIssue]
        user.save()# pyright: ignore[reportUnknownMemberType]
        logger.info("Updated stored password for username=%s", username)
    else:
        logger.debug("User already exists with unchanged password for username=%s", username)

    return cast(User, user)


def get_username_password(user_id: int) -> tuple[str, str]:
    logger.debug("Fetching username/password for user_id=%s", user_id)
    user: User = User.select().where(User.id == user_id).get() # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
    return user.username, user.password # pyright: ignore[reportUnknownVariableType, reportReturnType, reportUnknownMemberType]


def generate_links_data(
    team_id: str, event_id: str, user_id: str, presence: bool
) -> str:
    logger.debug(
        "Generating link token (team_id=%s, event_id=%s, user_id=%s, presence=%s)",
        team_id,
        event_id,
        user_id,
        presence,
    )
    user: User = User.select().where(User.id == user_id).get() # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
    return generate_hash(
        team_id, event_id, user.id, user.username, user.password, user.salt, presence
    )
