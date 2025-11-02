"""Module used to communicate with the Strava API"""

import logging
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests

from .assets import User
from .confs import Conf
from .postgres import Postgres

logger = logging.getLogger(__name__)


class Strava:
    """Strava class to communicate with the API"""

    def __init__(self, conf: Conf, postgres: Postgres):
        self.conf = conf
        self.postgres = postgres
        self.pause_until = None

    def get_token(self, client_code: str) -> Optional[dict]:
        """Gets the token to connect to the API as the current user"""
        res = requests.post(
            url=self.conf.STRAVA["get_token"]["url"],
            params=self.conf.STRAVA["get_token"]["params"] | {"code": client_code},
            timeout=10,
        )

        if res.status_code == 200:
            logger.debug("POST access token OK")
            return res.json()

        logger.warning(f"POST access token error : {res.status_code}")
        return None

    def refresh_token(self, refresh_token: str) -> Optional[dict]:
        """Gets the token to connect to the API as the current user"""
        res = requests.post(
            url=self.conf.STRAVA["get_refresh_token"]["url"],
            params=self.conf.STRAVA["get_refresh_token"]["params"]
            | {"refresh_token": refresh_token},
            timeout=10,
        )

        if res.status_code == 200:
            logger.debug("POST refresh token OK")
            return res.json()

        logger.warning(f"POST refresh token error : {res.status_code}")
        return None

    def get_activities_ids(self, user: User, page: int = 1) -> list[str]:
        """
        Gets the list of activities from the current user,
        which may lack of precision according to user preferences
        """
        self.wait_if_necessary()
        self.update_bearer_if_necessary(user)

        res = requests.get(
            url=self.conf.STRAVA["get_activities"]["url"],
            params=self.conf.STRAVA["get_activities"]["params"] | {"page": page},
            headers={"Authorization": f"Bearer {user.strava_access_token}"},
            timeout=10,
        )
        self.is_spamming(res)

        if res.status_code == 200:
            data = res.json()
            logger.debug(
                f"GET list activites : {len(data)} activities found at page {page}"
            )
            activities = [str(activity["id"]) for activity in data]
            if len(data) == self.conf.STRAVA["get_activities"]["params"]["per_page"]:
                activities.extend(self.get_activities_ids(user, page + 1))

            return activities

        logger.warning(f"GET list activities error : {res.status_code}")
        return {}

    def get_activity(self, user: User, activity_id: str) -> dict:
        """Gets a given activity with precise track"""
        self.wait_if_necessary()
        self.update_bearer_if_necessary(user)

        res = requests.get(
            url=self.conf.STRAVA["get_activity"]["url"].format(id=activity_id),
            headers={"Authorization": f"Bearer {user.strava_access_token}"},
            timeout=10,
        )
        self.is_spamming(res)

        if res.status_code == 200:
            data = res.json()
            logger.debug(f"GET activity {activity_id} OK : {data['name']}")
            return {
                "email": user.email,
                "id": data["id"],
                "sport": data["sport_type"],
                "name": data["name"],
                "description": data["description"],
                "track": data["map"]["polyline"],
                "start_date": datetime.fromisoformat(
                    data["start_date_local"].replace(
                        "Z", re.search(r"[-+]\d{2}:\d{2}", data["timezone"]).group()
                    )
                ),
                "distance": data["distance"],
                "duration": timedelta(seconds=data["elapsed_time"]),
                "speed": data["average_speed"],
                "elevation": data["total_elevation_gain"],
            }

        logger.warning(f"GET activity {activity_id} error : {res.status_code}")
        return {}

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

        logger.debug(
            "API Usage :\n"
            + f"X-RateLimit [15min] : {used[0]}/{limits[0]} : {round(used_percent[0] * 100, 2)}%\n"  # pylint: disable=line-too-long
            + f"X-RateLimit [daily] : {used[1]}/{limits[1]} : {round(used_percent[1] * 100, 2)}%\n"  # pylint: disable=line-too-long
            + f"X-ReadRateLimit [15min] : {used[2]}/{limits[2]} : {round(used_percent[2] * 100, 2)}%\n"  # pylint: disable=line-too-long
            + f"X-ReadRateLimit [daily] : {used[3]}/{limits[3]} : {round(used_percent[3] * 100, 2)}%"  # pylint: disable=line-too-long
        )

        now = datetime.now(timezone.utc)
        # Pauses until tomorrow 00:00 UTC
        if max(used_percent[1], used_percent[3]) > self.conf.STRAVA["spam_limit"]:
            self.pause_until = (now + timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

        # Pauses until next 15 minutes interval
        elif max(used_percent[0], used_percent[2]) > self.conf.STRAVA["spam_limit"]:
            next_quarter = (now.minute // 15 + 1) * 15
            if next_quarter == 60:
                self.pause_until = (now + timedelta(hours=1)).replace(
                    minute=0, second=0, microsecond=0
                )
            else:
                self.pause_until = now.replace(
                    minute=next_quarter, second=0, microsecond=0
                )

        if self.pause_until:
            logger.info(
                "Next API call will be put on hold until "
                + self.pause_until.strftime("%d/%m/%Y %H:%M:%S UTC"),
            )

    def wait_if_necessary(self):
        """Waits if necessary to prevent to spam the API"""
        if self.pause_until:
            if (
                to_wait := (
                    self.pause_until - datetime.now(timezone.utc)
                ).total_seconds()
            ) > 0:
                logger.info(
                    f"Waiting {round(to_wait)} seconds until "
                    + self.pause_until.strftime("%d/%m/%Y %H:%M:%S UTC")
                )
                time.sleep(to_wait)
        self.pause_until = None

    def update_bearer_if_necessary(self, user: User):
        """Calls get_token with the refresh_token if the current one has expired"""
        if user.strava_expires_date < datetime.now():
            logger.debug("Access token expired")
            refreshed_token = self.refresh_token(user.strava_refresh_token)
            user.strava_access_token = refreshed_token["access_token"]
            user.strava_expires_date = datetime.fromtimestamp(
                refreshed_token["expires_at"]
            )
            user.strava_refresh_token = refreshed_token["refresh_token"]
            self.postgres.update_user_details(
                user,
                {
                    "strava_access_token": user.strava_access_token,
                    "strava_expires_date": user.strava_expires_date,
                    "strava_refresh_token": user.strava_refresh_token,
                },
            )
