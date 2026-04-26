import logging
import uuid
from io import StringIO

import flask
import pytest


import app as app_module
from calendar_connector.logging_correlation import (
    CORRELATION_ID_HEADER,
    DEFAULT_CORRELATION_ID,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_DATEFMT,
    apply_correlation_formatter_to_logger_handlers,
    get_correlation_id,
    set_correlation_id,
    clear_correlation_id,
)


@pytest.fixture(autouse=True)
def reset_correlation_id_context() -> None:
    clear_correlation_id()
    yield
    clear_correlation_id()


def test_reuses_incoming_correlation_id_for_logs_and_response(
    monkeypatch,
    caplog,
) -> None:
    def fake_request_handler() -> flask.Response:
        logging.getLogger("calendar_connector.sporteasy_connector").info(
            "fake connector log"
        )
        logging.getLogger("calendar_connector.calendar_converter").info(
            "fake converter log"
        )
        return flask.Response("ok")

    monkeypatch.setattr(app_module, "request_handler", fake_request_handler)

    with app_module.app.test_client() as client, caplog.at_level(logging.INFO):
        response = client.get("/api", headers={CORRELATION_ID_HEADER: "cid-test-123"})

    assert response.status_code == 200
    assert response.headers[CORRELATION_ID_HEADER] == "cid-test-123"

    targeted_records = [
        record
        for record in caplog.records
        if record.getMessage() in {"fake connector log", "fake converter log"}
    ]
    assert len(targeted_records) == 2
    assert all(record.correlation_id == "cid-test-123" for record in targeted_records)


def test_generates_uuid_correlation_id_when_missing(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        app_module,
        "request_handler",
        lambda: flask.Response("ok"),
    )

    with app_module.app.test_client() as client:
        response = client.get("/api")

    assert response.status_code == 200
    response_correlation_id = response.headers[CORRELATION_ID_HEADER]
    assert str(uuid.UUID(response_correlation_id)) == response_correlation_id


def test_correlation_id_context_is_cleared_after_request(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        app_module,
        "request_handler",
        lambda: flask.Response("ok"),
    )

    with app_module.app.test_client() as client:
        response = client.get("/api", headers={CORRELATION_ID_HEADER: "cid-clear-test"})

    assert response.status_code == 200
    assert get_correlation_id() == "cid-clear-test"


def test_logs_outside_request_use_default_correlation_id(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logging.getLogger("test.outside").info("outside-request-log")

    outside_record = next(
        record
        for record in caplog.records
        if record.getMessage() == "outside-request-log"
    )
    assert outside_record.correlation_id == DEFAULT_CORRELATION_ID


def test_werkzeug_log_uses_pending_request_correlation_id(caplog) -> None:
    set_correlation_id("cid-werkzeug")

    with caplog.at_level(logging.INFO):
        logging.getLogger("werkzeug").info("access-log")
        logging.getLogger("test.after-werkzeug").info("post-access-log")

    werkzeug_record = next(
        record for record in caplog.records if record.getMessage() == "access-log"
    )
    assert werkzeug_record.correlation_id == "cid-werkzeug"

    post_access_record = next(
        record for record in caplog.records if record.getMessage() == "post-access-log"
    )
    assert post_access_record.correlation_id == "cid-werkzeug"


def test_flask_logger_output_contains_correlation_id() -> None:
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    test_logger = logging.getLogger("test.flask.logger.format")
    test_logger.handlers = [handler]
    test_logger.propagate = False
    test_logger.setLevel(logging.INFO)

    apply_correlation_formatter_to_logger_handlers(
        test_logger,
        fmt=DEFAULT_LOG_FORMAT,
        datefmt=DEFAULT_LOG_DATEFMT,
    )

    set_correlation_id("cid-format-test")
    try:
        test_logger.info("formatted-log")
    finally:
        clear_correlation_id()

    rendered_log = stream.getvalue()
    assert "correlation_id=cid-format-test" in rendered_log
