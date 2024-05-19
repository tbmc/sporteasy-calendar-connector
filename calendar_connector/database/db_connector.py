from pathlib import Path
from typing import Optional

from peewee import SqliteDatabase

from utils import is_under_unittest

_default_db_path = Path(__file__).parent.parent.parent / "database.db"

_database: Optional[SqliteDatabase] = None


def get_db() -> SqliteDatabase:
    global _database

    if _database is None:
        _database = _initiate_db()

    return _database


def _initiate_db() -> SqliteDatabase:
    if is_under_unittest():
        db = SqliteDatabase(":memory:")
    else:
        db = SqliteDatabase(_default_db_path)

    db.connect(reuse_if_open=True)
    return db
