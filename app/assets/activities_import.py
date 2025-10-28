"""Module used to manage the Activities Import asset"""

from celery.result import AsyncResult


class ActivitiesImport:
    """Activities Import class"""

    SCHEMA = (
        "email",
        "last_task_id",
        "last_start_date",
        "last_end_date",
    )

    def __init__(self, import_details: dict):
        self.email = import_details["email"]
        self.task_id = import_details["task_id"]
        self.last_start_date = import_details["last_start_date"]
        self.last_end_date = import_details["last_end_date"]

    def is_complete(self) -> bool:
        """Is the last logged import complete"""
        return self.last_start_date < self.last_end_date

    def is_running(self) -> bool:
        """Is the last logged import still running"""
        return AsyncResult(self.task_id).state == "RUNNING"
