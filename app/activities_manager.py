"""Module used to manage the Activities Manager"""

import logging

from .assets import Activity, User
from .postgres import Postgres
from .strava import Strava

logger = logging.getLogger(__name__)


class ActivitiesManager:
    """Activities Manager class to create and retrieve the activities"""

    def __init__(self, postgres: Postgres, strava: Strava):
        self.postgres = postgres
        self.strava = strava

    def get_activities(self, user: User) -> list[Activity]:
        """Returns the activities of the given user"""
        return [
            Activity(activity_details)
            for activity_details in self.postgres.get_activities_details(user)
        ]

    def update_activities(self, user: User):
        """Imports the new activities, deletes the non-existing ones"""
        imported_ids = [activity.id for activity in self.get_activities(user)]
        available_ids = self.strava.get_activities_ids(user)
        logger.info(
            f"{len(imported_ids)} activity⸱ies in database & {len(available_ids)} activity⸱ies on API"  # pylint: disable=line-too-long
        )

        to_import = list(set(available_ids) - set(imported_ids))
        for activity_id in to_import:
            self.postgres.save_activity(
                Activity(self.strava.get_activity(user, activity_id))
            )

        to_delete = list(set(imported_ids) - set(available_ids))
        self.postgres.delete_activities(to_delete)
