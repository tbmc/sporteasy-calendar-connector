import time
import datetime


def get_current_timestamp() -> int:
    return int(time.time() / 10)


def get_current_datetime() -> datetime.datetime:
    return datetime.datetime.now()
