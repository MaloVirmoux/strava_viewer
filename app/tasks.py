"""Module used to run the async Celery tasks"""

from datetime import datetime

from celery import Celery

from .activities_manager import ActivitiesManager
from .assets import User
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


@celery_app.task(bind=True)
def synchronize_activities(self, user_details: dict) -> dict:
    """Synchronizes the activities from the Strava API to the database"""
    # De-serialize user
    user_details["strava_expires_date"] = datetime.fromtimestamp(
        user_details["strava_expires_date"]
    )
    return activities_manager.synchronize_activities(User(user_details), self)
