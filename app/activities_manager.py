"""Module used to manage the Activities Manager"""

from .assets import Activity
from .postgres import Postgres
from .strava import Strava


class ActivitiesManager:
    """Activities Manager class to create and retrieve the activities"""

    def __init__(self, postgres: Postgres, strava: Strava):
        self.postgres = postgres
        self.strava = strava

    def update_activities(self, email: str):
        """Imports the new activities, deletes the non-existing ones"""
        imported_ids = [a.id for a in self.get_imported_activities(email)]
        available_ids = [a.id for a in self.get_available_activities(email)]

        self.import_activities(available_ids not in imported_ids, email)
        self.delete_activites(imported_ids not in available_ids)

    def get_imported_activities(self, email: str) -> list[Activity]:
        """Gets the activities from the database associated with the provided email"""
        return [
            Activity(activity_details)
            for activity_details in self.postgres.get_activities(email)
        ]

    def get_available_activities(self, email: str) -> list[Activity]:
        """Gets the available activities from Strava"""
        return [
            Activity(activity_details)
            for activity_details in self.strava.get_activities(email)
        ]

    def import_activities(self, activity_ids: list[str], email: str):
        """Gets the activities from Strava and saves it in the database"""
        for activity_id in activity_ids:
            self.postgres.save_activity(
                Activity({"email": email} | self.strava.get_activity(activity_id))
            )

    def delete_activites(self, activities: list[str]):
        """Deletes the activities from the database"""
        self.postgres.delete_activities([activity.id for activity in activities])
