"""Module used to run the async Celery tasks"""

from celery import Celery

from .activities_manager import ActivitiesManager
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

activities_manager = ActivitiesManager(postgres, strava)


@celery_app.task
def import_activites(email: str):
    """Imports the activities from the Strava API to the database"""
    activities_manager.update_activities(email)
