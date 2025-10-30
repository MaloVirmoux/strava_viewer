"""Module used to communicate with the JS and run the app"""

import argparse
import logging

logging_levels = {
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "debug": logging.DEBUG,
}
parser = argparse.ArgumentParser()
parser.add_argument("--log", choices=list(logging_levels.keys()), default="info")
parser.add_argument("--env", choices=["local", "container"], default="container")
args = parser.parse_args()

logging.basicConfig(level=logging_levels[args.log])
logger = logging.getLogger(__name__)

# pylint: disable=wrong-import-position
import urllib.parse
from datetime import datetime
from typing import cast

import flask
import flask_login
from argon2 import PasswordHasher
from celery import Celery
from dotenv import load_dotenv
from flask_cors import CORS

from .activities_manager import ActivitiesManager
from .assets import User
from .confs import SQL, Conf
from .postgres import Postgres
from .strava import Strava
from .users_manager import UsersManager

# pylint: enable=wrong-import-position

logger.debug("Loading environment variables & conf")
load_dotenv(f"{args.env}.env")
CONF = Conf()

logger.debug("Creating Flask app & initiate login tools")
app = flask.Flask(__name__)
CORS(app)

app.secret_key = CONF.FLASK["secret_key"]
login_manager = flask_login.LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)

current_user = cast(User, flask_login.current_user)

password_hasher = PasswordHasher()

logger.debug("Creating Celery app")
celery_app = Celery(
    "tasks",
    broker=CONF.REDIS["broker_url"],
    backend=CONF.REDIS["result_backend_url"],
)

logger.debug("Creating connectors to Postgres database & Strava API")
sql = SQL()
postgres = Postgres(CONF, sql)
strava = Strava(CONF, postgres)

activities_manager = ActivitiesManager(postgres, strava)
users_manager = UsersManager(postgres, password_hasher)


@login_manager.user_loader
def load_user(user_email):
    """Mandatory flask function to get the user"""
    return users_manager.get_user(user_email)


@app.route("/", methods=["GET"])
def index():
    """GET returns the homepage is the user is anonymous, or the userpage if he's logged in"""
    if current_user.is_authenticated:
        logger.debug("Redirecting to /home")
        return flask.redirect(flask.url_for("home"))

    logger.debug("Rendering /index")
    return flask.render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """GET returns the login webpage\n
    POST logs in the user to the website"""
    if flask.request.method == "GET":
        if current_user.is_authenticated:
            logger.debug("Redirecting to /home")
            return flask.redirect(flask.url_for("home"))

        logger.debug("Rendering /login")
        return flask.render_template("login.html")

    if flask.request.method == "POST":
        if users_manager.login_user(
            flask.request.form["email"], flask.request.form["password"]
        ):
            logger.debug(f"Form approved : Login user {flask.request.form['email']}")
            flask_login.login_user(
                users_manager.get_user(flask.request.form["email"]),
                remember=True,
                duration=CONF.FLASK["session_duration"],
            )
            logger.debug("Redirecting to /home")
            return flask.redirect(flask.url_for("home"))

        logger.warning("Form refused")
        flask.flash("Wrong email and/or password, please retry")
        logger.debug("Redirecting to /login")
        return flask.redirect(flask.url_for("login"))

    return None


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """GET returns the sign up webpage\n
    POST creates a new user"""
    if flask.request.method == "GET":
        # If there's a valid client_code, render step 2
        if client_code := flask.request.args.get("code"):
            if token := strava.get_token(client_code):
                logger.debug("Strava client_code approved : Moving on to step 2")
                flask.session["strava_user_id"] = token["athlete"]["id"]
                flask.session["profile_picture_url"] = token["athlete"]["profile"]
                flask.session["strava_access_token"] = token["access_token"]
                flask.session["strava_expires_date"] = datetime.fromtimestamp(
                    token["expires_at"]
                )
                flask.session["strava_refresh_token"] = token["refresh_token"]

                logger.debug("Rendernig /sign_up at step 2")
                return flask.render_template(
                    "sign_up.html",
                    step=2,
                    firstname=token["athlete"]["firstname"],
                    lastname=token["athlete"]["lastname"],
                )

            logger.warning("Strava client_code refused")
            flask.flash("Strava sign up was unsuccessful, please retry")

        # Else render step 1
        strava_login_url = "{url}?{params}".format(
            url=CONF.STRAVA["access_oauth"]["url"],
            params=urllib.parse.urlencode(CONF.STRAVA["access_oauth"]["params"]),
        )

        logger.debug("Rendering /sign_up at step 1")
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
            "import_task_id": None,
        }
        if user := users_manager.create_user(user_details):
            logger.debug(f"Form approved, login in user {flask.request.form['email']}")
            flask_login.login_user(
                user,
                remember=True,
                duration=CONF.FLASK["session_duration"],
            )
            logger.debug("Redirecting to /home")
            return flask.redirect(flask.url_for("home"))

        logger.warning("Form refused")
        flask.flash("An error occured, please retry")
        logger.debug("Redirecting to /sign_up at step 1")
        return flask.redirect(flask.url_for("sign_up"))

    return None


@app.route("/logout", methods=["GET"])
def logout():
    """GET logs out the user from the website"""
    logger.debug(f"Logout user {current_user.email}")
    flask_login.logout_user()
    logger.debug("Redirecting to /index")
    return flask.redirect(flask.url_for("index"))


@app.route("/home", methods=["GET"])
@flask_login.login_required
def home():
    """GET returns the userpage if he's logged in"""
    logger.debug(f"Rendering /home for {current_user.email}")
    activities = activities_manager.get_activities(current_user)

    if task_id := current_user.import_task_id:
        task = celery_app.AsyncResult(task_id)
        if task.state in ["PENDING", "SUCCESS"]:
            task_id = None

    logger.debug(f"HOME : {task_id}")

    return flask.render_template(
        "home.html",
        firstname=current_user.firstname,
        lastname=current_user.lastname,
        profile_picture_url=current_user.profile_picture_url,
        number_of_activities=len(activities),
        last_update=max(activity.start_date for activity in activities).strftime(
            "%Y/%m/%d - %H:%M"
        ),
        task_id=task_id,
    )


@app.route("/synchronize_activities", methods=["PUT"])
@flask_login.login_required
def synchronize_activities():
    """PUT synchronizes the activites of the user from Strava"""
    from . import tasks  # pylint: disable=import-outside-toplevel

    if task_id := current_user.import_task_id:
        task = celery_app.AsyncResult(task_id)
        if task.state not in ["PENDING", "SUCCESS"]:
            logger.info(f"Synchronize activity⸱ies : Task {task_id} found")
            return task_id
        logger.debug(f"Revoking task {task_id}")
        task.revoke()

    task_id = tasks.synchronize_activities.delay(current_user.to_dict()).id
    logger.info(f"Synchronize activity⸱ies : Task {task_id} created")
    users_manager.update_user(current_user, {"import_task_id": task_id})
    return task_id


@app.route("/task_status/<task_id>", methods=["GET"])
def task_status(task_id):
    """GET status of the provided task_id"""
    task = celery_app.AsyncResult(task_id)
    match task.state:
        case "PENDING" | "RETRY":
            res = {
                "state": task.state,
                "status": "Waiting for the task",
            }
        case "STARTED" | "PROGRESS":
            res = {
                "state": task.state,
                "status": task.info.get("status", "Synchronization is starting"),
                "current": task.info.get("current", 0),
                "total": task.info.get("total", 1),
            }
        case "SUCCESS":
            res = {
                "state": task.state,
                "new_activities": task.info["new_activities"],
                "total_activities": task.info["total_activities"],
            }
        case "FAILURE":
            res = {
                "state": task.state,
                "status": str(task.info),
            }
    return flask.jsonify(res)


if __name__ == "__main__":
    app.run(host=CONF.FLASK["host"], debug=True)
