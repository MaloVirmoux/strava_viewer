"""Module used to communicate with the Strava API"""

import requests

from python.connectors import Postgres
from python.utils import Conf


class Strava:
    """Strava class to communicate with the API"""

    def __init__(self, conf: Conf, postgres: Postgres):
        self.conf = conf
        self.postgres = postgres

    def get_token(self) -> dict:
        """Gets the token to connect to the API as the current user"""
        res = requests.post(
            url=self.conf.strava_token["url"],
            params=self.conf.strava_token["params"],
            timeout=10,
        )

        return res.json()
