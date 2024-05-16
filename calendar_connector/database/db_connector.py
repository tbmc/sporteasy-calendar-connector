from pathlib import Path

from peewee import SqliteDatabase

database_path = Path(__file__).parent.parent.parent / "database.db"

db = SqliteDatabase(database_path)
