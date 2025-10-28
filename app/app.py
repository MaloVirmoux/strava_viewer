"""Module used to communicate with the JS and run the app"""

import argparse
import datetime
import urllib.parse

import flask
import flask_login
from argon2 import PasswordHasher
from dotenv import load_dotenv
from flask_cors import CORS

from .activities_imports_manager import ActivitiesImportsManager
from .confs import SQL, Conf
from .postgres import Postgres
from .strava import Strava
from .users_manager import UsersManager

# Load env & conf
parser = argparse.ArgumentParser()
parser.add_argument("--env", choices=["local", "container"], default="container")
load_dotenv(f"{parser.parse_args().env}.env")
CONF = Conf()

# Create app & init login tools
app = flask.Flask(__name__)
CORS(app)

app.secret_key = CONF.FLASK["secret_key"]
login_manager = flask_login.LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)

password_hasher = PasswordHasher()

# Create connectors
sql = SQL()
postgres = Postgres(CONF, sql)
strava = Strava(CONF, postgres)

users_manager = UsersManager(postgres, password_hasher)
activities_import_manager = ActivitiesImportsManager(postgres)


@login_manager.user_loader
def load_user(user_email):
    """Mandatory flask function to get the user"""
    return users_manager.get_user(user_email)


@app.route("/", methods=["GET"])
def index():
    """GET returns the homepage is the user is anonymous, or the userpage if he's logged in"""
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for("home"))

    return flask.render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """GET returns the login webpage\n
    POST logs in the user to the website"""
    if flask.request.method == "GET":
        if flask_login.current_user.is_authenticated:
            return flask.redirect(flask.url_for("home"))

        return flask.render_template("login.html")

    if flask.request.method == "POST":
        if users_manager.login_user(
            flask.request.form["email"], flask.request.form["password"]
        ):
            flask_login.login_user(
                users_manager.get_user(flask.request.form["email"]),
                remember=True,
                duration=CONF.FLASK["session_duration"],
            )
            return flask.redirect(flask.url_for("home"))

        flask.flash("Wrong email and/or password, please retry")
        return flask.redirect(flask.url_for("login"))

    return None


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """GET returns the sign up webpage\n
    POST creates a new user"""
    if flask.request.method == "GET":
        if client_code := flask.request.args.get("code"):
            CONF.STRAVA["get_token"]["params"]["code"] = client_code
            if token := strava.get_token():
                CONF.STRAVA["bearer_token"] = token["access_token"]

                flask.session["strava_user_id"] = token["athlete"]["id"]
                flask.session["profile_picture_url"] = token["athlete"]["profile"]
                flask.session["strava_access_token"] = token["access_token"]
                flask.session["strava_expires_date"] = datetime.datetime.fromtimestamp(
                    token["expires_at"]
                )
                flask.session["strava_refresh_token"] = token["refresh_token"]

                return flask.render_template(
                    "sign_up.html",
                    step=2,
                    firstname=token["athlete"]["firstname"],
                    lastname=token["athlete"]["lastname"],
                )

            flask.flash("Strava sign up was unsuccessful, please retry")

        strava_login_url = "{url}?{params}".format(
            url=CONF.STRAVA["access_oauth"]["url"],
            params=urllib.parse.urlencode(CONF.STRAVA["access_oauth"]["params"]),
        )

        return flask.render_template(
            "sign_up.html",
            step=1,
            strava_login_url=strava_login_url,
        )

    if flask.request.method == "POST":
        user_details = {
            "email": flask.request.form["email"],
            "password": flask.request.form["password"],
            "firstname": flask.request.form["firstname"],
            "lastname": flask.request.form["lastname"],
            "strava_user_id": flask.session["strava_user_id"],
            "profile_picture_url": flask.session["profile_picture_url"],
            "strava_access_token": flask.session["strava_access_token"],
            "strava_expires_date": flask.session["strava_expires_date"],
            "strava_refresh_token": flask.session["strava_refresh_token"],
        }
        if user := users_manager.create_user(user_details):
            flask_login.login_user(
                user,
                remember=True,
                duration=CONF.FLASK["session_duration"],
            )
            return flask.redirect(flask.url_for("home"))

        flask.flash("An error occured, please retry")
        return flask.redirect(flask.url_for("sign_up"))

    return None


@app.route("/logout", methods=["GET"])
def logout():
    """GET logs out the user from the website"""
    flask_login.logout_user()
    return flask.redirect(flask.url_for("index"))


@app.route("/home", methods=["GET"])
@flask_login.login_required
def home():
    """GET returns the userpage if he's logged in"""
    user = flask_login.current_user
    return flask.render_template(
        "home.html",
        firstname=user.firstname,
        lastname=user.lastname,
        profile_picture_url=user.profile_picture_url,
        number_of_activities=2,
        last_update=datetime.datetime.now().strftime("%Y/%m/%d - %H:%M"),
    )


@app.route("/update_activities", methods=["PUT"])
@flask_login.login_required
def update_activities():
    """PUT updates the activites of the user from Strava"""
    activities_import_manager.import_user_activities(flask_login.current_user.email)


if __name__ == "__main__":
    app.run(host=CONF.FLASK["host"], debug=True)
