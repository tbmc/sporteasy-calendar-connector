import logging
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
_pending_werkzeug_correlation_id_ctx: ContextVar[str] = ContextVar(
    "pending_werkzeug_correlation_id", default=DEFAULT_CORRELATION_ID
)
_base_log_record_factory = logging.getLogRecordFactory()
_is_log_record_factory_installed = False


def generate_correlation_id() -> str:
    return str(uuid.uuid4())


def set_correlation_id(correlation_id: str | None) -> str:
    value = correlation_id.strip() if correlation_id is not None else ""
    if value == "":
        value = generate_correlation_id()
    _correlation_id_ctx.set(value)
    return value


def get_correlation_id() -> str:
    return _correlation_id_ctx.get()


def clear_correlation_id() -> None:
    _correlation_id_ctx.set(DEFAULT_CORRELATION_ID)


def set_pending_werkzeug_correlation_id(correlation_id: str) -> None:
    _pending_werkzeug_correlation_id_ctx.set(correlation_id)


def pop_pending_werkzeug_correlation_id() -> str:
    correlation_id = _pending_werkzeug_correlation_id_ctx.get()
    _pending_werkzeug_correlation_id_ctx.set(DEFAULT_CORRELATION_ID)
    return correlation_id


def install_correlation_log_record_factory() -> None:
    global _is_log_record_factory_installed
    if _is_log_record_factory_installed:
        return

    def correlation_log_record_factory(*args: Any, **kwargs: Any) -> logging.LogRecord:
        record = _base_log_record_factory(*args, **kwargs)
        correlation_id = get_correlation_id()
        if (
            correlation_id == DEFAULT_CORRELATION_ID
            and record.name.startswith("werkzeug")
        ):
            pending = pop_pending_werkzeug_correlation_id()
            if pending != DEFAULT_CORRELATION_ID:
                correlation_id = pending

        record.correlation_id = correlation_id  # type: ignore[attr-defined]
        return record

    logging.setLogRecordFactory(correlation_log_record_factory)
    _is_log_record_factory_installed = True


def apply_correlation_formatter_to_logger_handlers(
    logger: logging.Logger,
    fmt: str = DEFAULT_LOG_FORMAT,
    datefmt: str = DEFAULT_LOG_DATEFMT,
) -> None:
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    for handler in logger.handlers:
        handler.setFormatter(formatter)
