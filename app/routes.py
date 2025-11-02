"""Module used to define the Flask routes"""

import logging
import urllib
from datetime import datetime
from typing import cast

import flask
import flask_login
from celery import Celery
from celery.app.task import Task

from .activities_manager import ActivitiesManager
from .assets import User
from .confs import Conf
from .users_manager import UsersManager

logger = logging.getLogger(__name__)

current_user = cast(User, flask_login.current_user)


class Routes:
    """Routes class to define the Flask webpages"""

    def __init__(
        self,
        conf: Conf,
        users_manager: UsersManager,
        activities_manager: ActivitiesManager,
        celery_app: Celery,
    ):
        self.conf = conf
        self.users_manager = users_manager
        self.activities_manager = activities_manager
        self.celery_app = celery_app

    def index(self):
        """GET returns /index is the user is anonymous,
        or /home if he's logged in"""
        if current_user.is_authenticated:
            logger.debug("Redirecting to /home")
            return flask.redirect(flask.url_for("home"))

        logger.debug("Rendering /index")
        return flask.render_template("index.html")

    def login(self):
        """GET returns /login\n
        POST logs in the user to the website"""
        if flask.request.method == "GET":
            if current_user.is_authenticated:
                logger.debug("Redirecting to /home")
                return flask.redirect(flask.url_for("home"))

            logger.debug("Rendering /login")
            return flask.render_template("login.html")

        if flask.request.method == "POST":
            if self.users_manager.login_user(
                flask.request.form["email"], flask.request.form["password"]
            ):
                logger.debug(
                    f"Form approved : Login user {flask.request.form['email']}"
                )
                flask_login.login_user(
                    self.users_manager.get_user(flask.request.form["email"]),
                    remember=True,
                    duration=self.conf.FLASK["session_duration"],
                )
                logger.debug("Redirecting to /home")
                return flask.redirect(flask.url_for("home"))

            logger.warning("Form refused")
            flask.flash("Wrong email and/or password, please retry")
            logger.debug("Redirecting to /login")
            return flask.redirect(flask.url_for("login"))

        return None

    def sign_up(self):
        """GET returns /sign_up\n
        POST creates a new user"""
        if flask.request.method == "GET":
            # If there's a valid client_code, render step 2
            if client_code := flask.request.args.get("code"):
                if token := self.activities_manager.strava.get_token(client_code):
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
                url=self.conf.STRAVA["access_oauth"]["url"],
                params=urllib.parse.urlencode(
                    self.conf.STRAVA["access_oauth"]["params"]
                ),
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
            if user := self.users_manager.create_user(user_details):
                logger.debug(
                    f"Form approved, login in user {flask.request.form['email']}"
                )
                flask_login.login_user(
                    user,
                    remember=True,
                    duration=self.conf.FLASK["session_duration"],
                )
                logger.debug("Redirecting to /home")
                return flask.redirect(flask.url_for("home"))

            logger.warning("Form refused")
            flask.flash("An error occured, please retry")
            logger.debug("Redirecting to /sign_up at step 1")
            return flask.redirect(flask.url_for("sign_up"))

        return None

    def logout(self):
        """GET logs out the user from the website,
        and redirects to /index"""
        logger.debug(f"Logout user {current_user.email}")
        flask_login.logout_user()
        logger.debug("Redirecting to /index")
        return flask.redirect(flask.url_for("index"))

    def home(self):
        """GET returns /home if he's logged in"""
        logger.debug(f"Rendering /home for {current_user.email}")
        activities = self.activities_manager.get_activities(current_user)

        if task_id := current_user.import_task_id:
            task = self.celery_app.AsyncResult(task_id)
            if task.state in ["PENDING", "SUCCESS"]:
                task_id = None

        logger.debug(f"HOME : {task_id}")

        return flask.render_template(
            "home.html",
            firstname=current_user.firstname,
            lastname=current_user.lastname,
            profile_picture_url=current_user.profile_picture_url,
            number_of_activities=len(activities),
            last_import=max(activity.start_date for activity in activities).strftime(
                "%Y/%m/%d - %H:%M"
            ),
            task_id=task_id,
        )

    def synchronize_activities(self, process: Task):
        """PUT synchronizes the activites of the user from Strava"""
        if task_id := current_user.import_task_id:
            task = self.celery_app.AsyncResult(task_id)
            if task.state not in ["PENDING", "FAILURE", "SUCCESS"]:
                logger.info(f"Synchronize activity⸱ies : Task {task_id} found")
                return task_id
            logger.debug(f"Revoking task {task_id}")
            task.revoke()

        task_id = process.delay(current_user.to_dict()).id
        logger.info(f"Synchronize activity⸱ies : Task {task_id} created")
        self.users_manager.update_user(current_user, {"import_task_id": task_id})
        return task_id

    def task_status(self, task_id: str):
        """GET the status of the provided task_id"""
        task = self.celery_app.AsyncResult(task_id)
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
