"""Module used to represent the user"""


class User:
    """User class with mandatory flask funtions"""

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
