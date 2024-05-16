from calendar_connector.database.db_connector import db
from calendar_connector.database.user import User

if __name__ == "__main__":
    db.create_tables([User])
