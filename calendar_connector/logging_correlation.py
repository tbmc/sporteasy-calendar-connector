import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any

CORRELATION_ID_HEADER = "X-Correlation-ID"
DEFAULT_CORRELATION_ID = "-"
DEFAULT_LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - "
    "[correlation_id=%(correlation_id)s] - %(message)s"
)
DEFAULT_LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"

_correlation_id_ctx: ContextVar[str] = ContextVar(
    "correlation_id", default=DEFAULT_CORRELATION_ID
)
_base_log_record_factory = logging.getLogRecordFactory()
_is_log_record_factory_installed = False
DEFAULT_LEVEL = logging.DEBUG

formatter = logging.Formatter(
    DEFAULT_LOG_FORMAT,
    datefmt=DEFAULT_LOG_DATEFMT,
)


def generate_correlation_id() -> str:
    return str(uuid.uuid4())


def set_correlation_id(correlation_id: str | None) -> str:
    value = correlation_id.strip() if correlation_id is not None else ""
    if value == "":
        value = generate_correlation_id()
    _correlation_id_ctx.set(value)
    return value


def get_correlation_id() -> str:
    correlation_id = _correlation_id_ctx.get(None)
    if correlation_id is None or correlation_id.strip() == "":
        return "∅"
    return correlation_id


def clear_correlation_id() -> None:
    _correlation_id_ctx.set(DEFAULT_CORRELATION_ID)


class CorrelationIdJsonFieldsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        print("LOGGING !!!")
        correlation_id = get_correlation_id()
        record.correlation_id = correlation_id
        return True


def setup_correlation_logging() -> None:
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(DEFAULT_LEVEL)

    log_handler.setFormatter(formatter)

    logging.basicConfig(level=DEFAULT_LEVEL, handlers=[log_handler])


def install_correlation_log_record_factory() -> None:
    global _is_log_record_factory_installed
    if _is_log_record_factory_installed:
        return

    def correlation_log_record_factory(*args: Any, **kwargs: Any) -> logging.LogRecord:
        record = _base_log_record_factory(*args, **kwargs)
        correlation_id = get_correlation_id()
        record.correlation_id = correlation_id
        return record

    logging.setLogRecordFactory(correlation_log_record_factory)
    _is_log_record_factory_installed = True


def apply_correlation_formatter_to_logger_handlers(
    logger: logging.Logger,
) -> None:
    for handler in logger.handlers:
        handler.setFormatter(formatter)
        handler.addFilter(CorrelationIdJsonFieldsFilter())
