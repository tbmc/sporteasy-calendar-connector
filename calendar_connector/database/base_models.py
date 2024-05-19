from peewee import Model

from database.db_connector import get_db

db = get_db()


class BaseModel(Model):
    class Meta:
        database = db
