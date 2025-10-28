"""Module used to communicate with the Strava API"""

import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests

from .confs import Conf
from .postgres import Postgres


class Strava:
    """Strava class to communicate with the API"""

    def __init__(self, conf: Conf, postgres: Postgres):
        self.conf = conf
        self.postgres = postgres
        self.pause_until = None

    def get_token(self) -> Optional[dict]:
        """Gets the token to connect to the API as the current user"""
        res = requests.post(
            url=self.conf.STRAVA["get_token"]["url"],
            params=self.conf.STRAVA["get_token"]["params"],
            timeout=10,
        )

        if res.status_code == 200:
            return res.json()

        return None

    def get_activities(self, email: str, page: int = 1) -> list[dict]:
        """
        Gets the list of activities from the current user,
        which may lack of precision according to user preferences
        """
        self.wait_if_necessary()

        res = requests.get(
            url=self.conf.STRAVA["get_activities"]["url"],
            params=self.conf.STRAVA["get_activities"]["params"] | {"page": page},
            headers={
                "Authorization": f"Bearer {self.conf.STRAVA["strava_bearer_token"]}"
            },
            timeout=10,
        )
        self.is_spamming(res)

        data = res.json()
        activities = [activity["id"] for activity in data]
        if len(data) == self.conf.STRAVA["get_activities"]["params"]["per_page"]:
            activities.extend(self.get_activities(email, page + 1))

        return activities

    def get_activity(self, activity_id) -> dict:
        """Gets a given activity with precise track"""
        self.wait_if_necessary()

        res = requests.get(
            url=self.conf.STRAVA["get_activity"]["url"].format(id=activity_id),
            headers={
                "Authorization": f"Bearer {self.conf.STRAVA["strava_bearer_token"]}"
            },
            timeout=10,
        )
        self.is_spamming(res)
        data = res.json()
        return {
            "id": data["id"],
            "sport": data["sport_type"],
            "name": data["name"],
            "description": data["description"],
            "track": data["map"]["polyline"],
            "start_date": data["start_date_local"],
            "distance": data["distance"],
            "duration": data["elapsed_time"],
            "speed": data["average_speed"],
            "elevation": data["total_elevation_gain"],
        }

    def is_spamming(self, res: requests.Response):
        """Checks from the headers if the API is spammed"""
        headers = res.headers

        def header_to_list(header):
            return list(map(int, header.split(",")))

        limits = header_to_list(
            f"{headers['x-ratelimit-limit']},{headers['x-readratelimit-limit']}"
        )
        used = header_to_list(
            f"{headers['x-ratelimit-usage']},{headers['x-readratelimit-usage']}"
        )
        used_percent = [used[i] / limits[i] for i in range(4)]

        now = datetime.now(timezone.utc)
        if max([used_percent[1]], used_percent[3]) > self.conf.STRAVA.spam_limit:
            self.pause_until = (now + timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif max([used_percent[0]], used_percent[2]) > self.conf.STRAVA.spam_limit:
            next_quarter = (now.minute // 15 + 1) * 15
            if next_quarter == 60:
                self.pause_until = (now + timedelta(hours=1)).replace(
                    minute=0, second=0, microsecond=0
                )
            else:
                self.pause_until = now.replace(
                    minute=next_quarter, second=0, microsecond=0
                )

    def wait_if_necessary(self):
        """Waits if necessary to prevent to spam the API"""
        if self.pause_until:
            if (to_wait := (self.pause_until - datetime.now()).total_seconds()) > 0:
                time.sleep(to_wait)
        self.pause_until = None
