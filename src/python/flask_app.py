from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from conf import Conf
from api.strava import login_to_strava

# Create app
app = Flask(__name__)
CORS(app)

# Load env & conf
load_dotenv()
conf = Conf()
conf.strava_token["params"]["client_secret"] = os.environ["CLIENT_SECRET"]


@app.route("/")
def home():
    return "Hello world"


@app.route("/get_token", methods=["GET"])
def login():
    client_code = request.args.get("client_code")
    conf.strava_token["params"]["code"] = client_code
    login_to_strava(conf)

    return jsonify(reply=f"Received: {client_code}")


if __name__ == "__main__":
    app.run(debug=True)
