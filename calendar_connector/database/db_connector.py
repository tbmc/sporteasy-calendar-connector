from pathlib import Path
from typing import Optional
import logging

from peewee import SqliteDatabase

from calendar_connector.utils import is_under_unittest

_default_db_path = Path(__file__).parent.parent.parent / "database.db"

logger = logging.getLogger(__name__)

_database: Optional[SqliteDatabase] = None


def get_db() -> SqliteDatabase:
    global _database

    if _database is None:
        logger.debug("Initializing database connection")
        _database = _initiate_db()

    return _database


def _initiate_db() -> SqliteDatabase:
    if is_under_unittest():
        logger.info("Using in-memory sqlite database for tests")
        db = SqliteDatabase(":memory:")
    else:
        logger.info("Using sqlite database at path=%s", _default_db_path)
        db = SqliteDatabase(_default_db_path)

    db.connect(reuse_if_open=True)
    logger.debug("Database connection established")
    return db
