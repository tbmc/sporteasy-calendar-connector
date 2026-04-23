from typing import Optional
import logging

from peewee import SqliteDatabase

from calendar_connector.database.db_connector import get_db
from calendar_connector.database.all_models import ALL_MODELS

logger = logging.getLogger(__name__)


def create_db(db: Optional[SqliteDatabase] = None) -> None:
    if db is None:
        db = get_db()
    logger.info("Creating database tables (%s models)", len(ALL_MODELS))
    db.create_tables(ALL_MODELS) # pyright: ignore[reportUnknownMemberType]
    logger.debug("Database tables created")


if __name__ == "__main__":
    create_db()
    print("Created tables")
