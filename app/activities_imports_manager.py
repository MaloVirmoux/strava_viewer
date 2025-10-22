"""Module used to manage the ActivitiesImports Manager"""

from typing import Optional

from celery.result import AsyncResult

from .assets import ActivitiesImport
from .postgres import Postgres


class ActivitiesImportsManager:
    """Import Logs Manager class to create and retrieve the imports"""

    def __init__(self, postgres: Postgres):
        self.postgres = postgres

    def import_user_activities(self, email: str) -> AsyncResult:
        """Imports all the new activities from the user"""
        last_import = self.get_last_import(email)
        if last_import and not last_import.is_complete():
            task = AsyncResult(last_import.task_id)
            if task.state == "RUNNING":
                return task
            task.revoke()

        # pylint: disable-next=import-outside-toplevel
        from . import tasks

        return tasks.import_activites.delay(email)

    def get_last_import(self, email: str) -> Optional[ActivitiesImport]:
        """Gets the import associated with the provided email"""
        if import_details := self.postgres.get_activities_import(email):
            return ActivitiesImport(import_details)
        return None
