"""Module used to communicate with the JS and run the backend app"""

import datetime

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

from connectors import Postgres, Strava
from utils import SQL, Conf

# Create app
app = Flask(__name__)
CORS(app)

# Load env & conf
load_dotenv()
conf = Conf()

# Create connectors
sql = SQL()
postgres = Postgres(conf, sql)
strava = Strava(conf, postgres)


@app.route("/login", methods=["GET"])
def login():
    """Login the user onto Strava"""
    client_code = request.args.get("client_code")
    conf.strava_token["params"]["code"] = client_code
    token = strava.get_token()

    conf.strava_bearer_token = token["access_token"]

    username = f'{token["athlete"]["firstname"]} {token["athlete"]["lastname"]}'.strip()
    postgres.save_user(
        {
            "user_id": token["athlete"]["id"],
            "user_name": username,
            "access_token": token["access_token"],
            "expires_date": datetime.datetime.fromtimestamp(token["expires_at"]),
            "refresh_token": token["refresh_token"],
            "last_connection": datetime.datetime.now(),
        }
    )

    return username


@app.route("/get_activites", methods=["GET"])
def get_activites_list():
    """Gets all the activites from the user"""
    is_not_empty = True
    page = 1
    activites_list = []
    while is_not_empty:
        new_activities = strava.get_activities_list(page)
        is_not_empty = (
            len(new_activities) == conf.strava_activities_list["params"]["per_page"]
        )
        activites_list.extend(new_activities)
        page = page + 1

    return activites_list


if __name__ == "__main__":
    app.run(debug=True)
