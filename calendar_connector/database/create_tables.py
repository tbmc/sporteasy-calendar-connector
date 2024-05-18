from peewee import SqliteDatabase

from calendar_connector.database.user import User
from calendar_connector.database.db_connector import get_db


def create_db() -> SqliteDatabase:
    db = get_db()
    db.create_tables([User])
    return db


if __name__ == "__main__":
    create_db()
