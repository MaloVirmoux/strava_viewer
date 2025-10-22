"""Module used to communicate with the PostgreSQL Database"""

from typing import Any, Dict, Optional, Tuple

import psycopg2

from .assets import ActivitiesImport, User
from .confs import SQL, Conf


class Postgres:
    """PostgreSQL class to communicate with the database"""

    def __init__(self, conf: Conf, sql: SQL):
        self.conf = conf
        self.sql = sql
        self.connection = self._create_new_connection()

    def _create_new_connection(self):
        return psycopg2.connect(
            database=self.conf.POSTGRES["database"],
            host=self.conf.POSTGRES["host"],
            port=self.conf.POSTGRES["port"],
            user=self.conf.POSTGRES["user"],
            password=self.conf.POSTGRES["password"],
        )

    # ========== UTILS ==========

    def res_to_dict(self, res: Optional[Tuple], schema: Tuple) -> dict:
        """Converts a SQL response to a dictionary according to the provided schema"""
        if isinstance(res, Tuple):
            return dict(zip(schema, res))
        return {}

    def dict_to_sql(self, column_value: dict) -> str:
        """Converts a dictionary to a SQL string for update queries"""
        return ", ".join(
            [f"{column} = '{value}'" for column, value in column_value.items()]
        )

    # ========== USERS ==========

    def create_user(self, user: User) -> User:
        """Saves the user into the table `users`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.insert_user, vars(user))

        self.connection.commit()
        return user

    def get_user(self, email: str) -> Dict[str, Any]:
        """Gets the user from the table `users`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.get_user, {"email": email})
            res = cursor.fetchone()

        return self.res_to_dict(res, User.SCHEMA)

    def update_user(self, email: str, values: dict):
        """Updates the data in the table `users`, values is dict {"column_name" : "new_value"}"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.sql.update_user,
                vars({"email": email, "value": self.dict_to_sql(values)}),
            )

        self.connection.commit()

    # ========== ACTIVITIES IMPORTS ==========

    def create_activities_import(
        self, activities_import: ActivitiesImport
    ) -> ActivitiesImport:
        """Saves the activities_import into the table `activities_imports`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.insert_activities_import, vars(activities_import))

        self.connection.commit()
        return activities_import

    def get_activities_import(self, email: str) -> Dict[str, Any]:
        """Gets the import from the table"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.get_activities_import, {"email": email})
            res = cursor.fetchone()

        return self.res_to_dict(res, ActivitiesImport.SCHEMA)

    def update_activities_import(self, email: str, values: dict):
        # pylint: disable-next=line-too-long
        """Updates the data in the table `activities_imports`, values is dict {"column_name" : "new_value"}"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.sql.update_activities_import,
                vars({"email": email, "value": self.dict_to_sql(values)}),
            )
        self.connection.commit()

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
