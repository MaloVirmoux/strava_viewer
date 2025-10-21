"""Module used to create the conf both from the static values and the environment"""

import datetime
import os


class Conf:
    """Conf class"""

    def __init__(self):
        self.FLASK = {
            "host": os.environ["FLASK_HOST"],
            "secret_key": os.environ["FLASK_SECRET_KEY"],
            "session_duration": datetime.timedelta(days=90),
        }

        self.POSTGRES = {
            "database": os.environ["POSTGRES_DB"],
            "user": os.environ["POSTGRES_USER"],
            "password": os.environ["POSTGRES_PASSWORD"],
            "host": os.environ["POSTGRES_HOST"],
            "port": 5432,
        }

        self.REDIS = {
            "broker_url": os.environ["REDIS_BROKER_URL"],
            "result_backend_url": os.environ["REDIS_RESULT_BACKEND_URL"],
        }

        self.STRAVA = {
            "access_oauth": {
                "url": "https://www.strava.com/oauth/authorize",
                "params": {
                    "client_id": "169921",
                    "redirect_uri": "http://localhost:5000/sign_up",
                    "response_type": "code",
                    "approval_prompt": "auto",
                    "scope": "activity:read",
                },
            },
            "get_token": {
                "url": "https://www.strava.com/api/v3/oauth/token",
                "params": {
                    "client_id": "169921",
                    "client_secret": os.environ["STRAVA_CLIENT_SECRET"],
                    "code": None,
                    "grant_type": "authorization_code",
                },
            },
            "bearer_token": None,
            "get_activities_list": {
                "url": "https://www.strava.com/api/v3/athlete/activities",
                "params": {
                    "before": None,
                    "after": None,
                    "page": None,
                    "per_page": 100,
                },
            },
        }
