from typing import cast

from peewee import Model, PrimaryKeyField, CharField

from calendar_connector.cryptography import generate_salt, generate_hash
from calendar_connector.database import db


class User(Model):
    id = PrimaryKeyField()
    username = CharField(unique=True, max_length=256, null=False)
    password = CharField(max_length=256, null=False)
    salt = CharField(max_length=51, null=False)

    class Meta:
        database = db


def save_user(username: str, password: str) -> User:
    already_existing_user = list(User.select().where(User.username == username))

    if len(already_existing_user) == 0:
        user = User(username=username, password=password, salt=generate_salt())
        user.save()
        return user

    return cast(User, already_existing_user[0])


def get_username_password(user_id: int) -> tuple[str, str]:
    user = User.select().where(User.id == user_id).get()
    return user.username, user.password


def generate_links_data(event_id: str, user_id: str) -> str:
    user = User.select().where(User.id == user_id).get()
    return generate_hash(event_id, user.id, user.username, user.password, user.salt)
