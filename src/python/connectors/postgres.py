"""Module used to communicate with the PostgreSQL Database"""

import psycopg2

from python.utils import SQL, Conf


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
        """Saves the loged-in user onto the database"""
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql.format(self.sql.user_login, user_data))
            updated_row_count = cursor.rowcount

        self.connection.commit()
        return updated_row_count
