"""Module used to communicate with the PostgreSQL Database"""

from typing import Any, Dict, Optional, Tuple

import psycopg2

from .assets import Activity, User
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
        """Converts a dictionary to a SQL string for UPDATE queries"""
        return ", ".join(
            [f"{column} = '{value}'" for column, value in column_value.items()]
        )

    def tuple_to_sql(self, values: tuple) -> str:
        """Converts a tuple to a SQL string for IN queries"""
        return ", ".join([f"'{value}'" for value in values])

    # ========== USERS ==========

    def save_user(self, user: User) -> User:
        """Saves the user into the table `users`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.insert_user, vars(user))

        self.connection.commit()
        return user

    def get_user_details(self, email: str) -> Dict[str, Any]:
        """Gets the user from the table `users`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.get_user, {"email": email})
            res = cursor.fetchone()

        return self.res_to_dict(res, User.SCHEMA)

    def update_user_details(self, email: str, details: dict):
        """Updates the data in the table `users`, details is dict {"column_name" : "new_value"}"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.sql.update_user,
                vars({"email": email, "details": self.dict_to_sql(details)}),
            )

        self.connection.commit()

    # ========== ACTIVITIES ==========

    def save_activity(self, activity: Activity) -> Activity:
        """Saves the activity into the table `activities`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.insert_activity, vars(activity))

        self.connection.commit()
        return activity

    def get_activities_details(self, email: str) -> Dict[str, Any]:
        """Gets the activities details from the table `activities`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.get_activities, {"email": email})
            res = cursor.fetchall()

        return [self.res_to_dict(row, Activity.SCHEMA) for row in res]

    def delete_activities(self, ids: list):
        """Deletes activities from the table `activities` given a list of ids"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.delete_activities, {"ids": self.tuple_to_sql(ids)})

        self.connection.commit()
