"""Module used to run the async Celery tasks"""

import datetime

from celery import Celery

from .confs import SQL, Conf
from .postgres import Postgres
from .strava import Strava

CONF = Conf()
celery_app = Celery(
    "tasks",
    broker=CONF.REDIS["broker_url"],
    backend=CONF.REDIS["result_backend_url"],
)

sql = SQL()
postgres = Postgres(CONF, sql)
strava = Strava(CONF, postgres)


@celery_app.task
def import_activites(email: str):
    """Imports the activities from the Strava API to the database"""
    postgres.update_activities_import(
        email, {"last_start_date": datetime.datetime.now()}
    )
