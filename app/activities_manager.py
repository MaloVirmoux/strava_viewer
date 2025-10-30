"""Module used to manage the Activities Manager"""

import logging

from celery.app.task import Task

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

    def synchronize_activities(self, user: User, task: Task) -> dict:
        """Imports the new activities, deletes the non-existing ones"""
        task.update_state(
            state="PROGRESS", meta={"status": "Retrieving the list of activities"}
        )
        imported_ids = [activity.id for activity in self.get_activities(user)]
        available_ids = self.strava.get_activities_ids(user)
        if to_import := list(set(available_ids) - set(imported_ids)):
            logger.info(
                f"{len(imported_ids)} activity⸱ies in database &"
                + f"{len(available_ids)} activity⸱ies on API : "
                + f"{len(to_import)} activity⸱ies import"
            )

            for i, activity_id in enumerate(to_import[:5]):
                task.update_state(
                    state="PROGRESS",
                    meta={
                        "status": f"Importing new activities : {i}/{len(to_import)}",
                        "current": i,
                        "total": len(to_import),
                    },
                )
                self.postgres.save_activity(
                    Activity(self.strava.get_activity(user, activity_id))
                )

        if to_delete := list(set(imported_ids) - set(available_ids)):
            task.update_state(
                state="PROGRESS", meta={"status": "Cleaning old activities"}
            )
            self.postgres.delete_activities(to_delete)

        return {
            "new_activities": len(to_import),
            "total_activities": len(imported_ids) + len(to_import) - len(to_delete),
        }
