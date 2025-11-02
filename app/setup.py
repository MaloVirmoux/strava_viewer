"""Module used to setup the imports and the apps"""

# ========== Imports ==========

import logging
import os

import flask
import flask_login
from argon2 import PasswordHasher
from celery import Celery
from dotenv import load_dotenv
from flask_cors import CORS

from .activities_manager import ActivitiesManager
from .confs import SQL, Conf
from .postgres import Postgres
from .routes import Routes
from .strava import Strava
from .users_manager import UsersManager

# ========== Logging &  Conf ==========

logger = logging.getLogger(__name__)
logger.debug("Loading environment variables & conf")
load_dotenv(f"{os.environ['running_env']}.env")
CONF = Conf()

# ========== Managers ==========

logger.debug("Creating users & activities managers")
sql = SQL()
postgres = Postgres(CONF, sql)
strava = Strava(CONF, postgres)

password_hasher = PasswordHasher()
users_manager = UsersManager(postgres, password_hasher)
activities_manager = ActivitiesManager(postgres, strava)

# ========== Celery App ==========

logger.debug("Creating Celery app")
celery_app = Celery(
    "tasks",
    broker=CONF.REDIS["broker_url"],
    backend=CONF.REDIS["result_backend_url"],
)

# ========== Flask App ==========

logger.debug("Creating Flask app & initiate login tools")
flask_app = flask.Flask(__name__)
CORS(flask_app)

flask_app.secret_key = CONF.FLASK["secret_key"]
login_manager = flask_login.LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(flask_app)

routes = Routes(CONF, users_manager, activities_manager, celery_app)
