"""Module used to communicate with the JS and run the backend app"""

import datetime
import json
import urllib.parse
import flask
import flask_login
from argon2 import PasswordHasher
from dotenv import load_dotenv
from flask_cors import CORS

from assets import User
from connectors import Postgres, Strava
from loaders import SQL, Conf

# Load env & conf
load_dotenv()
conf = Conf()

# Create app & init login tools
app = flask.Flask(__name__)
CORS(app)

app.secret_key = conf.flask["secret_key"]
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

password_hasher = PasswordHasher()

# Create connectors
sql = SQL()
postgres = Postgres(conf, sql)
strava = Strava(conf, postgres)

HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_UNAUTHORIZE = 401
HTTP_STATUS_UNACCEPTABLE = 406
JSON_TYPE = "application/json"

SESSION_DURATION = datetime.timedelta(days=conf.flask["session_duration"])


@login_manager.user_loader
def load_user(user_email):
    try:
        user = User(postgres, user_email)
    except AssertionError:
        return None
    return user

@app.route("/", methods=["GET"])
def index():
    return flask.render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return flask.render_template("login.html")
    
    elif flask.request.method == "POST":
        """Login into an existing user"""
        login_details = flask.request.get_json()
        user = User(postgres, login_details["email"])

        if password_hasher.verify(user.password, login_details["password"]):
            flask_login.login_user(user, remember=True, duration=SESSION_DURATION)
            return flask.Response(status=HTTP_STATUS_OK)

        return flask.Response(status=HTTP_STATUS_UNAUTHORIZE)

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """Create a new user"""
    if flask.request.method == "GET":
        strava_login_url = "{url}?{query_params}".format(url=conf.strava_oauth["url"], query_params=urllib.parse.urlencode(conf.strava_oauth["params"]))

        return flask.render_template("sign_up.html", strava_login_url=strava_login_url)
    
    if flask.request.method == "POST": 
        user_details = flask.request.get_json()
        user_details["strava_user_id"] = flask.session["strava_user_id"]
        user_details["strava_access_token"] = flask.session["strava_access_token"]
        user_details["strava_expires_date"] = flask.session["strava_expires_date"]
        user_details["strava_refresh_token"] = flask.session["strava_refresh_token"]

        user = User(postgres)
        try:
            user.create(user_details, password_hasher)
        except AssertionError as e:
            return flask.Response(
                json.dumps({"exception": str(e)}),
                status=HTTP_STATUS_UNACCEPTABLE,
                content_type=JSON_TYPE,
            )

        return flask.Response(status=HTTP_STATUS_CREATED)

@app.route("/get_strava_token", methods=["GET"])
def get_strava_token():
    """Login the user onto Strava"""
    client_code = flask.request.args.get("client_code")
    conf.strava_token["params"]["code"] = client_code
    status, token = strava.get_token()

    if status:
        conf.strava_bearer_token = token["access_token"]

        flask.session["strava_user_id"] = token["athlete"]["id"]
        flask.session["strava_access_token"] = token["access_token"]
        flask.session["strava_expires_date"] = datetime.datetime.fromtimestamp(
            token["expires_at"]
        )
        flask.session["strava_refresh_token"] = token["refresh_token"]

        response = {
            "status": True,
            "firstname": token["athlete"]["firstname"],
            "lastname": token["athlete"]["lastname"],
        }

        return flask.Response(
            json.dumps(response), status=HTTP_STATUS_OK, content_type=JSON_TYPE
        )
    else:
        response = {"status": False}
        return flask.Response(
            json.dumps(response),
            status=HTTP_STATUS_UNAUTHORIZE,
            content_type=JSON_TYPE,
        )

@app.route("/home", methods=["GET"])
@flask_login.login_required
def home():
    user = flask_login.current_user
    return flask.render_template("home.html", firstname=user.firstname, lastname=user.lastname)

# To do : Continue get activities, manage response in case of error
# @app.route("/get_activites", methods=["GET"])
# def get_activites_list():
#     """Gets all the activites from the user"""
#     is_not_empty = True
#     page = 1
#     activites_list = []
#     while is_not_empty:
#         new_activities = strava.get_activities_list(page)
#         is_not_empty = (
#             len(new_activities) == conf.strava_activities_list["params"]["per_page"]
#         )
#         activites_list.extend(new_activities)
#         page = page + 1

#     return flask.Response(activites_list)


if __name__ == "__main__":
    app.run(debug=True)
