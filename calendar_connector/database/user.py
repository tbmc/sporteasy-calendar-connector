from typing import cast

from peewee import PrimaryKeyField, CharField

from calendar_connector.cryptography import generate_salt, generate_hash
from calendar_connector.custom_exceptions import TooManyUsersException
from calendar_connector.database.base_models import BaseModel


class User(BaseModel):
    id = PrimaryKeyField()
    username = CharField(unique=True, max_length=256, null=False)
    password = CharField(max_length=256, null=False)
    salt = CharField(max_length=51, null=False)


def save_user(username: str, password: str) -> User:
    already_existing_users = list(User.select().where(User.username == username))

    if len(already_existing_users) > 1:
        raise TooManyUsersException(username, len(already_existing_users))

    if len(already_existing_users) == 0:
        user = User(username=username, password=password, salt=generate_salt())
        user.save()
        return user

    user = already_existing_users[0]
    if user.password != password:
        user.password = password  # type: ignore
        user.save()

    return cast(User, user)


def get_username_password(user_id: int) -> tuple[str, str]:
    user = User.select().where(User.id == user_id).get()
    return user.username, user.password


def generate_links_data(
    team_id: str, event_id: str, user_id: str, presence: bool
) -> str:
    user = User.select().where(User.id == user_id).get()
    return generate_hash(
        team_id, event_id, user.id, user.username, user.password, user.salt, presence
    )
