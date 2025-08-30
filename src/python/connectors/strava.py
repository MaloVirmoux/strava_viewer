"""Module used to communicate with the Strava API"""

import requests

from connectors import Postgres
from utils import Conf


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

    def get_activities_list(self, page: int) -> list:
        """
        Gets the list of activities from the current user,
        which may lack of precision according to user preferences
        """
        params = self.conf.strava_activities_list["params"]
        params["page"] = page
        res = requests.get(
            url=self.conf.strava_activities_list["url"],
            params=params,
            headers={"Authorization": f"Bearer {self.conf.strava_bearer_token}"},
            timeout=10,
        )

        return res.json()
