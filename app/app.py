"""Module used to run the apps"""

import flask_login

from . import setup_env

if __name__ == "__main__":
    setup_env()

# pylint: disable=wrong-import-position
from . import tasks
from .setup import celery_app  # pylint: disable=unused-import
from .setup import CONF, flask_app, login_manager, routes, users_manager

# pylint: enable=wrong-import-position


@login_manager.user_loader
def load_user(user_email):
    """Mandatory flask function to get the user"""
    return users_manager.get_user(user_email)


@flask_app.route("/", methods=["GET"])
def index():
    """GET returns /index is the user is anonymous,
    or /home if he's logged in"""
    return routes.index()


@flask_app.route("/login", methods=["GET", "POST"])
def login():
    """GET returns /login\n
    POST logs in the user to the website"""
    return routes.login()


@flask_app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """GET returns /sign_up\n
    POST creates a new user"""
    return routes.sign_up()


@flask_app.route("/logout", methods=["GET"])
def logout():
    """GET logs out the user from the website,
    and redirects to /index"""
    return routes.logout()


@flask_app.route("/home", methods=["GET"])
@flask_login.login_required
def home():
    """GET returns /home if he's logged in"""
    return routes.home()


@flask_app.route("/synchronize_activities", methods=["PUT"])
@flask_login.login_required
def synchronize_activities():
    """PUT synchronizes the activites of the user from Strava"""
    return routes.synchronize_activities(tasks.synchronize_activities)


@flask_app.route("/task_status/<task_id>", methods=["GET"])
def task_status(task_id: str):
    """GET the status of the provided task_id"""
    return routes.task_status(task_id)


if __name__ == "__main__":
    flask_app.run(host=CONF.FLASK["host"], debug=True)
