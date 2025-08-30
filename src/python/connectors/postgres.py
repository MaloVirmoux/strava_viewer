"""Module used to communicate with the PostgreSQL Database"""

import datetime
from typing import Tuple

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

    def get_user(self, user_id: int) -> Tuple[bool, int]:
        """Gets a user conncetion status and his token"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.sql.format_request(self.sql.get_user, {"user_id": user_id})
            )
            res = cursor.fetchone()

        try:
            assert isinstance(res, Tuple)
            _, access_token, expires_date, refresh_token = res
        except AssertionError as e:
            raise AssertionError(f"User {user_id} has not been found") from e

        if expires_date > datetime.datetime.now():
            return (True, access_token)
        return (False, refresh_token)

    def save_user(self, user_data: dict) -> int:
        """Saves the loged-in user onto the database"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.format_request(self.sql.user_login, user_data))
            updated_row_count = cursor.rowcount

        self.connection.commit()
        return updated_row_count

    def get_activities(
        self,
        *,
        user_id: int,
        from_date=None,
        to_date=None,
        min_lat=None,
        max_lat=None,
        min_long=None,
        max_long=None,
    ) -> pl.DataFrame:
        """Returns the activities from the user as a Polar DataFrame"""
        activities_filter = {
            "user_id": user_id,
            "from_date": from_date,
            "to_date": to_date,
            "min_lat": min_lat,
            "max_lat": max_lat,
            "min_long": min_long,
            "max_long": max_long,
        }
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.sql.format_request(self.sql.user_login, activities_filter)
            )

        self.connection.commit()
        return pl.DataFrame()
