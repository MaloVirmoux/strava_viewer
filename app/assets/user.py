"""Module used to manage the user"""

import re
from typing import Any, Dict, Optional

from argon2 import PasswordHasher
from connectors import Postgres

EMAIL_REGEX = r"^\S+@\S+\.[a-zA-Z]{2,}$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class User:
    """User class with both mandatory flask funtions and database management"""

    def __init__(self, postgres: Postgres, email: Optional[str] = None):
        self.postgres = postgres
        self.verified = False

        if email:
            self.get(email)

    def create(self, user_details: Dict[str, Any], password_hasher: PasswordHasher):
        self.set_details(user_details)

        self.verify_email()
        self.verify_password()
        self.verify_if_user_already_exists()

        self.password = password_hasher.hash(self.password)
        self.save()

    def get(self, email: str):
        user_details = self.postgres.get_user(email)
        if user_details:
            self.set_details(user_details)
            self.verified = True
        else:
            raise NonExistingUserException(email)

    def set_details(self, user_details: Dict[str, Any]):
        self.email = user_details["email"]
        self.password = user_details["password"]
        self.firstname = user_details["firstname"]
        self.lastname = user_details["lastname"]
        self.strava_user_id = user_details["strava_user_id"]
        self.profile_picture_url = user_details["profile_picture_url"]
        self.strava_access_token = user_details["strava_access_token"]
        self.strava_expires_date = user_details["strava_expires_date"]
        self.strava_refresh_token = user_details["strava_refresh_token"]

    def verify_email(self):
        is_email = bool(re.fullmatch(EMAIL_REGEX, self.email))
        if not is_email:
            raise InvalidEmailException

    def verify_password(self):
        is_password_strong = re.fullmatch(PASSWORD_REGEX, self.password)
        if not is_password_strong:
            raise UnsecurePasswordException

    def verify_if_user_already_exists(self):
        if self.postgres.get_user(self.email):
            raise ExistingUserException(self.email)

    def save(self):
        self.postgres.save_user(
            {
                "email": self.email,
                "password": self.password,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "strava_user_id": self.strava_user_id,
                "profile_picture_url": self.profile_picture_url,
                "strava_access_token": self.strava_access_token,
                "strava_expires_date": self.strava_expires_date,
                "strava_refresh_token": self.strava_refresh_token,
            }
        )

    def is_authenticated(self):
        return self.verified

    def is_active(self):
        return self.verified

    def is_anonymous(self):
        return not self.verified

    def get_id(self):
        return self.email


class InvalidEmailException(AssertionError):
    """Custom exception for invalid emails"""

    def __init__(self, *args: object) -> None:
        super().__init__("The provided email is not valid", *args)


class UnsecurePasswordException(AssertionError):
    """Custom exception for invalid passwords"""

    def __init__(self, *args: object) -> None:
        super().__init__("The provided password is not valid", *args)


class ExistingUserException(AssertionError):
    """Custom exception for existing user"""

    def __init__(self, identifier: str, *args: object) -> None:
        super().__init__(
            f"An user already exists with the provided identifier : {identifier}",
            *args,
        )


class NonExistingUserException(AssertionError):
    """Custom exception for non existing user"""

    def __init__(self, identifier: str, *args: object) -> None:
        super().__init__(
            f"No user exists with the provided identifier : {identifier}", *args
        )
