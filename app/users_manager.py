"""Module used to manage the Users Manager"""

import re
from typing import Any, Dict, Optional

import argon2

from .assets import User
from .postgres import Postgres

EMAIL_REGEX = r"^\S+@\S+\.[a-zA-Z]{2,}$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class UsersManager:
    """Users Manager class to create and retrieve the users"""

    def __init__(self, postgres: Postgres, password_hasher: argon2.PasswordHasher):
        self.postgres = postgres
        self.password_hasher = password_hasher

    def get_user(self, email: str) -> Optional[User]:
        """Gets the user associated with the provided email"""
        if user_details := self.postgres.get_user_details(email):
            return User(user_details)
        return None

    def login_user(self, email: str, password: str) -> bool:
        """Checks the login of a user"""
        user = self.get_user(email)
        try:
            self.password_hasher.verify(user.password, password)
        except argon2.exceptions.Argon2Error:
            return False
        return True

    def create_user(self, user_details: Dict[str, Any]) -> Optional[User]:
        """Creates a new user"""
        if (
            self.verify_email(user_details["email"])
            and self.verify_password(user_details["password"])
            and self.verify_if_user_already_exists(user_details["email"])
        ):
            user_details["password"] = self.hash_password(user_details["password"])
            return self.postgres.save_user(User(user_details))
        return None

    def verify_email(self, email: str):
        """Verifies if the provided email is valid"""
        return bool(re.fullmatch(EMAIL_REGEX, email))

    def verify_password(self, password: str):
        """Verifies if the provided password is secure"""
        return bool(re.fullmatch(PASSWORD_REGEX, password))

    def verify_if_user_already_exists(self, email: str):
        """Verifies if the user is already registered"""
        return not bool(self.get_user(email))

    def hash_password(self, password: str) -> str:
        """Hashes the password using argon2"""
        return self.password_hasher.hash(password)
