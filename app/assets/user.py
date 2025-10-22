"""Module used to manage the User asset"""


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
    )

    def __init__(self, user_details: dict):
        self.email = user_details["email"]
        self.password = user_details["password"]
        self.firstname = user_details["firstname"]
        self.lastname = user_details["lastname"]
        self.strava_user_id = user_details["strava_user_id"]
        self.profile_picture_url = user_details["profile_picture_url"]
        self.strava_access_token = user_details["strava_access_token"]
        self.strava_expires_date = user_details["strava_expires_date"]
        self.strava_refresh_token = user_details["strava_refresh_token"]

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
