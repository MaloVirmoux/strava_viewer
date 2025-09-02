"""Module used to communicate with the PostgreSQL Database"""

from typing import Any, Tuple

import polars as pl
import psycopg2
from utils import SQL, Conf


class Postgres:
    """PostgreSQL class to communicate with the database"""

    def __init__(self, conf: Conf, sql: SQL):
        self.conf = conf
        self.sql = sql
        self.connection = self._create_new_connection()

    def _create_new_connection(self):
        return psycopg2.connect(
            database=self.conf.postgres["database_name"],
            host="localhost",
            port=5432,
            user=self.conf.postgres["username"],
            password=self.conf.postgres["password"],
        )

    def save_tmp_user(self, strava_user_data: dict) -> int:
        """Saves the new user into the tmp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.sql.format_request(self.sql.save_tmp_user, strava_user_data)
            )
            updated_row_count = cursor.rowcount

        self.connection.commit()
        return updated_row_count

    def get_tmp_user(self, strava_user_id: int) -> dict[str, Any]:
        """Gets the user from the tmp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.sql.format_request(
                    self.sql.get_tmp_user, {"strava_user_id": strava_user_id}
                )
            )
            res = cursor.fetchone()

        try:
            assert isinstance(res, Tuple)
            _, strava_access_token, strava_expires_date, strava_refresh_token = res
        except AssertionError as e:
            raise NonExistingUserException(str(strava_user_id)) from e

        return {
            "strava_access_token": strava_access_token,
            "strava_expires_date": strava_expires_date,
            "strava_refresh_token": strava_refresh_token,
        }

    def delete_tmp_user(self, strava_user_id: int) -> int:
        """Deletes the user from the tmp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.sql.format_request(
                    self.sql.delete_tmp_user, {"strava_user_id": strava_user_id}
                )
            )
            updated_row_count = cursor.rowcount

        self.connection.commit()
        return updated_row_count

    def save_user(self, user_data: dict) -> int:
        """Saves the user into the table"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.format_request(self.sql.save_user, user_data))
            updated_row_count = cursor.rowcount

        self.connection.commit()
        return updated_row_count

    def get_user(self, email: str, expect_empty: bool = True) -> dict[str, Any]:
        """Gets the user from the table"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.format_request(self.sql.get_user, {"email": email}))
            res = cursor.fetchone()

        if expect_empty:
            if res is not None:
                raise ExistingUserException(email)
            return {}

        try:
            assert isinstance(res, Tuple)
            (
                _,
                password,
                session_key,
                firstname,
                lastname,
                strava_user_id,
                strava_access_token,
                strava_expires_date,
                strava_refresh_token,
            ) = res
        except AssertionError:
            raise NonExistingUserException(email)

        return {
            "password": password,
            "session_key": session_key,
            "firstname": firstname,
            "lastname": lastname,
            "strava_user_id": strava_user_id,
            "strava_access_token": strava_access_token,
            "strava_expires_date": strava_expires_date,
            "strava_refresh_token": strava_refresh_token,
        }

    #     self.connection.commit()
    #     return updated_row_count

    # def get_activities(
    #     self,
    #     *,
    #     user_id: int,
    #     from_date=None,
    #     to_date=None,
    #     min_lat=None,
    #     max_lat=None,
    #     min_long=None,
    #     max_long=None,
    # ) -> pl.DataFrame:
    #     """Returns the activities from the user as a Polar DataFrame"""
    #     activities_filter = {
    #         "user_id": user_id,
    #         "from_date": from_date,
    #         "to_date": to_date,
    #         "min_lat": min_lat,
    #         "max_lat": max_lat,
    #         "min_long": min_long,
    #         "max_long": max_long,
    #     }
    #     with self.connection.cursor() as cursor:
    #         cursor.execute(
    #             self.sql.format_request(self.sql.user_login, activities_filter)
    #         )

    #     self.connection.commit()
    #     return pl.DataFrame()


class ExistingUserException(AssertionError):
    """Custom exception for existing user"""

    def __init__(self, identifier: str, *args: object) -> None:
        super().__init__(
            f"An account already exists with the provided identifier : {identifier}",
            *args,
        )


class NonExistingUserException(AssertionError):
    """Custom exception for non existing user"""

    def __init__(self, identifier: str, *args: object) -> None:
        super().__init__(
            f"No account exists with the provided identifier : {identifier}", *args
        )
