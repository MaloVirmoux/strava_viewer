import requests


def login_to_strava(conf) -> dict:
    res = requests.post(
        url=conf.strava_token["url"],
        params=conf.strava_token["params"],
    )

    return res.json
