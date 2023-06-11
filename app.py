import flask
from calendar_converter import get_calendar_text
from dotenv import dotenv_values

app = flask.Flask(__name__)

env = dotenv_values(".env")


@app.route("/")
def main_request_handler() -> flask.Response:
    try:
        username = flask.request.args.get("username")
        password = flask.request.args.get("password")
        if username is None:
            username = env.get("username")
        if password is None:
            password = env.get("password")
        if username is None or not any(username) or password is None or not any(password):
            raise Exception("Missing username and password")

        calendar_text = get_calendar_text(username, password)

        return flask.Response(calendar_text, headers={
            "Content-Type": "text/calendar; charset=utf-8"
        })
    except Exception as e:
        return flask.Response(str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0")

