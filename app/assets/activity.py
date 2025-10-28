"""Module used to manage the Activity asset"""


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
        self.email = import_details["email"]
        self.id = import_details["id"]
        self.sport = import_details["sport"]
        self.name = import_details["name"]
        self.description = import_details["description"]
        self.track = import_details["track"]
        self.start_date = import_details["start_date"]
        self.distance = import_details["distance"]
        self.duration = import_details["duration"]
        self.speed = import_details["speed"]
        self.elevation = import_details["elevation"]
