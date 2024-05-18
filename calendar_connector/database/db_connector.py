from pathlib import Path
from typing import Optional

from peewee import SqliteDatabase


_default_db_path = Path(__file__).parent.parent.parent / "database.db"

_database: Optional[SqliteDatabase] = None


def get_db(db_path: Path = _default_db_path) -> SqliteDatabase:
    global _database

    if _database is None:
        _database = SqliteDatabase(db_path)
        _database.connect(reuse_if_open=True)

    return _database
