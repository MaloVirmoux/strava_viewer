"""Module used to communicate with the JS and run the backend app"""

import datetime
import json

from connectors import Postgres, Strava
from dotenv import load_dotenv
from flask import Flask, Response, request, session
from flask_cors import CORS
from utils import SQL, Account, Conf

from argon2 import PasswordHasher

# Create app
app = Flask(__name__)
CORS(app)

# Load tools
password_hasher = PasswordHasher()

# Load env & conf
load_dotenv()
conf = Conf()

# Create connectors
sql = SQL()
postgres = Postgres(conf, sql)
strava = Strava(conf, postgres)

HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_UNAUTHORIZE = 401
HTTP_STATUS_UNACCEPTABLE = 406
JSON_TYPE = "application/json"


@app.route("/login_to_strava", methods=["GET"])
def login_to_strava():
    """Login the user onto Strava"""
    client_code = request.args.get("client_code")
    conf.strava_token["params"]["code"] = client_code
    status, token = strava.get_token()

    if status:
        conf.strava_bearer_token = token["access_token"]

        postgres.save_tmp_user(
            {
                "strava_user_id": token["athlete"]["id"],
                "strava_access_token": token["access_token"],
                "strava_expires_date": datetime.datetime.fromtimestamp(
                    token["expires_at"]
                ),
                "strava_refresh_token": token["refresh_token"],
            }
        )
        response = {
            "status": True,
            "user_id": token["athlete"]["id"],
            "firstname": token["athlete"]["firstname"],
            "lastname": token["athlete"]["lastname"],
        }

        return Response(
            json.dumps(response), status=HTTP_STATUS_OK, content_type=JSON_TYPE
        )
    else:
        response = {"status": False}
        return Response(
            json.dumps(response),
            status=HTTP_STATUS_UNAUTHORIZE,
            content_type=JSON_TYPE,
        )


@app.route("/create_account", methods=["POST"])
def create_account():
    """Create a new user"""
    account_details = request.get_json()
    account = Account(postgres, password_hasher)
    try:
        account.create(account_details)
    except AssertionError as e:
        return Response(
            json.dumps({"exception": str(e)}),
            status=HTTP_STATUS_UNACCEPTABLE,
            content_type=JSON_TYPE,
        )

    return Response(status=HTTP_STATUS_CREATED)


# To do : Continue get activities, manage response in case of error
# @app.route("/get_activites", methods=["GET"])
# def get_activites_list():
#     """Gets all the activites from the user"""
#     is_not_empty = True
#     page = 1
#     activites_list = []
#     while is_not_empty:
#         new_activities = strava.get_activities_list(page)
#         is_not_empty = (
#             len(new_activities) == conf.strava_activities_list["params"]["per_page"]
#         )
#         activites_list.extend(new_activities)
#         page = page + 1

#     return Response(activites_list)


if __name__ == "__main__":
    app.run(debug=True)
