"""Module used to read the conf both from the files and the environment"""

import json
import os


class Conf:
    """Conf class to access the backend configuration"""

    def __init__(self):
        self.postgres = {}
        self.strava_oauth = {}
        self.strava_token = {}

        with open("../conf/connectors.json", "r", encoding="utf-8") as f:
            connectors_conf = json.load(f)

        for key, value in connectors_conf.items():
            setattr(self, key, value)

        self.postgres["password"] = os.environ["POSTGRES_PASSWORD"]
        self.strava_token["params"]["client_secret"] = os.environ["CLIENT_SECRET"]
