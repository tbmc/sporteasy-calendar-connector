from calendar_connector.database.db_connector import db

db.connect(reuse_if_open=True)
database = db
