import json


class Conf:
    def __init__(self):
        with open("../conf/login.json", "r") as f:
            login_conf = json.load(f)

        for key, value in login_conf.items():
            setattr(self, key, value)
