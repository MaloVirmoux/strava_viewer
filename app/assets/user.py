"""Module used to manage the User asset"""

from datetime import datetime


class User:
    """User class with mandatory flask functions"""

    SCHEMA = (
        "email",
        "password",
        "firstname",
        "lastname",
        "strava_user_id",
        "profile_picture_url",
        "strava_access_token",
        "strava_expires_date",
        "strava_refresh_token",
        "import_task_id",
    )

    def __init__(self, user_details: dict):
        self.email: str = user_details["email"]
        self.password: str = user_details["password"]
        self.firstname: str = user_details["firstname"]
        self.lastname: str = user_details["lastname"]
        self.strava_user_id: str = user_details["strava_user_id"]
        self.profile_picture_url: str = user_details["profile_picture_url"]
        self.strava_access_token: str = user_details["strava_access_token"]
        self.strava_expires_date: datetime = user_details["strava_expires_date"]
        self.strava_refresh_token: str = user_details["strava_refresh_token"]
        self.import_task_id: str = user_details["import_task_id"]

    def to_dict(self) -> dict:
        """Returns the user as a json serializable dict"""
        return {
            "email": self.email,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "strava_user_id": self.strava_user_id,
            "profile_picture_url": self.profile_picture_url,
            "strava_access_token": self.strava_access_token,
            "strava_expires_date": self.strava_expires_date.timestamp(),
            "strava_refresh_token": self.strava_refresh_token,
            "import_task_id": self.import_task_id,
        }

    def is_authenticated(self):
        """Mandatory flask function"""
        return True

    def is_active(self):
        """Mandatory flask function"""
        return True

    def is_anonymous(self):
        """Mandatory flask function"""
        return False

    def get_id(self):
        """Mandatory flask function"""
        return self.email
