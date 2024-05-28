from typing import Optional

from peewee import SqliteDatabase

from calendar_connector.database.db_connector import get_db
from calendar_connector.database.all_models import ALL_MODELS


def create_db(db: Optional[SqliteDatabase] = None) -> None:
    if db is None:
        db = get_db()
    db.create_tables(ALL_MODELS)


if __name__ == "__main__":
    create_db()
    print("Created tables")
