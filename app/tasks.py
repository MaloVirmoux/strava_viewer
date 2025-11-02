"""Module used to define the async Celery tasks"""

from datetime import datetime

from .assets import User
from .setup import activities_manager, celery_app


@celery_app.task(bind=True)
def synchronize_activities(self, user_details: dict) -> dict:
    """Synchronizes the activities from the Strava API to the database"""
    # De-serialize user
    user_details["strava_expires_date"] = datetime.fromtimestamp(
        user_details["strava_expires_date"]
    )
    return activities_manager.synchronize_activities(User(user_details), self)
