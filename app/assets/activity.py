"""Module used to manage the Activity asset"""

from datetime import datetime, timedelta


class Activity:
    """Activity class"""

    SCHEMA = (
        "email",
        "id",
        "sport",
        "name",
        "description",
        "track",
        "start_date",
        "distance",
        "duration",
        "speed",
        "elevation",
    )

    def __init__(self, import_details: dict):
        self.email: str = import_details["email"]
        self.id: str = import_details["id"]
        self.sport: str = import_details["sport"]
        self.name: str = import_details["name"]
        self.description: str = import_details["description"]
        self.track: str = import_details["track"]
        self.start_date: datetime = import_details["start_date"]
        self.distance: float = import_details["distance"]
        self.duration: timedelta = import_details["duration"]
        self.speed: float = import_details["speed"]
        self.elevation: float = import_details["elevation"]
