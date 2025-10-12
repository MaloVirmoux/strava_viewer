"""Module used to communicate with the PostgreSQL Database"""

from typing import Any, Dict, Tuple

import psycopg2

from loaders import SQL, Conf


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

    def save_user(self, user_data: dict) -> int:
        """Saves the user into the table"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.format_request(self.sql.save_user, user_data))
            updated_row_count = cursor.rowcount

        self.connection.commit()
        return updated_row_count

    def get_user(self, email: str) -> Dict[str, Any]:
        """Gets the user from the table"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.format_request(self.sql.get_user, {"email": email}))
            res = cursor.fetchone()

        if isinstance(res, Tuple):
            return dict(
                zip(
                    (
                        "email",
                        "password",
                        "firstname",
                        "lastname",
                        "strava_user_id",
                        "strava_access_token",
                        "strava_expires_date",
                        "strava_refresh_token",
                    ),
                    res
                )
            )

        return {}

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
