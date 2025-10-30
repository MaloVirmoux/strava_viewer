"""Module used to communicate with the PostgreSQL Database"""

import logging
from typing import Any, Dict, Optional, Tuple

import psycopg2

from .assets import Activity, User
from .confs import SQL, Conf

logger = logging.getLogger(__name__)


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

    def dict_keys_to_sql(self, column_value: dict) -> str:
        """Converts a dictionary to a SQL string for UPDATE queries"""
        return ", ".join([f"{column} = %({column})s" for column in column_value.keys()])

    def tuple_to_sql(self, values: tuple) -> str:
        """Converts a tuple to a SQL string for IN queries"""
        return ", ".join([f"'{value}'" for value in values])

    # ========== USERS ==========

    def save_user(self, user: User):
        """Saves the user into the table `users`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.insert_user, vars(user))
            self.connection.commit()

        logger.debug(f"User {user.email} saved to the database")

    def get_user_details(self, email: str) -> Dict[str, Any]:
        """Gets the user from the table `users`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.get_user, {"email": email})
            res = cursor.fetchone()

        logger.debug(f"Getting details from {email}")
        return self.res_to_dict(res, User.SCHEMA)

    def update_user_details(self, user: User, details: dict):
        """Updates the data in the table `users`, details is dict {"column_name" : "new_value"}"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.sql.update_user.format(columns=self.dict_keys_to_sql(details)),
                {"email": user.email} | details,
            )
            self.connection.commit()

        logger.debug(f"Updating detail⸱s {list(details.keys())} of user {user.email}")

    # ========== ACTIVITIES ==========

    def save_activity(self, activity: Activity):
        """Saves the activity into the table `activities`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.insert_activity, vars(activity))
            self.connection.commit()

        logger.debug(f"Activity {activity.id} saved to the database")

    def get_activities_details(self, user: User) -> list[dict[str, Any]]:
        """Gets the activities details from the table `activities`"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.get_activities, {"email": user.email})
            res = cursor.fetchall()

        logger.debug(f"Getting activity⸱ies from {user.email}")
        return [self.res_to_dict(row, Activity.SCHEMA) for row in res]

    def delete_activities(self, ids: list):
        """Deletes activities from the table `activities` given a list of ids"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.delete_activities, {"ids": self.tuple_to_sql(ids)})
            self.connection.commit()

        logger.debug(f"Deleting activity⸱ies {ids}")
