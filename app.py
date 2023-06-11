import flask
from calendar_converter import get_calendar_text

app = flask.Flask(__name__)


@app.route("/")
def main_request_handler() -> flask.Response:
    try:
        username = flask.request.args.get("username")
        password = flask.request.args.get("password")
        if username is None or not any(username) or password is None or not any(password):
            raise Exception("Missing username and password")

        calendar_text = get_calendar_text(username, password)

        return flask.Response(calendar_text)
    except Exception as e:
        return flask.Response(str(e))


