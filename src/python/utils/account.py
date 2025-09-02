"""Module used to manage the accounts in the database"""

import re
from typing import Any

# from connectors import Postgres

from argon2 import PasswordHasher

EMAIL_REGEX = r"^\S+@\S+\.[a-zA-Z]{2,}$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class Account:
    """Conf class to manage an account"""

    def __init__(self, postgres, password_hasher: PasswordHasher):
        self.postgres = postgres
        self.password_hasher = password_hasher

    def create(self, account_details: dict[str, Any]):
        self.email = account_details["email"]
        self.password = account_details["password"]
        self.firstname = account_details["firstname"]
        self.lastname = account_details["lastname"]
        self.strava_user_id = account_details["user_id"]

        self.strava_access_token = None
        self.strava_expires_date = None
        self.strava_refresh_token = None

        self.check_details()
        self.check_if_account_exists()
        self.search_strava_details()
        self.encode_password()
        self.save()
        self.delete_strava_details()

    def check_details(self):
        is_email = bool(re.fullmatch(EMAIL_REGEX, self.email))
        if not is_email:
            raise InvalidEmailException

        is_password_strong = re.fullmatch(PASSWORD_REGEX, self.password)
        if not is_password_strong:
            raise UnsecurePasswordException

    def check_if_account_exists(self):
        self.postgres.get_user(self.email, expect_empty=True)

    def search_strava_details(self):
        strava_details = self.postgres.get_tmp_user(self.strava_user_id)

        self.strava_access_token = strava_details["strava_access_token"]
        self.strava_expires_date = strava_details["strava_expires_date"]
        self.strava_refresh_token = strava_details["strava_refresh_token"]

    def encode_password(self):
        self.password = self.password_hasher.hash(self.password)

    def save(self):
        self.postgres.save_user(
            {
                "email": self.email,
                "password": self.password,
                "session_key": None,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "strava_user_id": self.strava_user_id,
                "strava_access_token": self.strava_access_token,
                "strava_expires_date": self.strava_expires_date,
                "strava_refresh_token": self.strava_refresh_token,
            }
        )

    def delete_strava_details(self):
        self.postgres.delete_tmp_user(self.strava_user_id)


class InvalidEmailException(AssertionError):
    """Custom exception for invalid emails"""

    def __init__(self, *args: object) -> None:
        super().__init__("The provided email is not valid", *args)


class UnsecurePasswordException(AssertionError):
    """Custom exception for invalid passwords"""

    def __init__(self, *args: object) -> None:
        super().__init__("The provided password is not valid", *args)
