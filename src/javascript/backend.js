import { loginToStrava, getActivites } from "./python_api";

import * as connectors_conf from "../conf/connectors.json";

// Updates the Strava login button URL
export function setStravaOAuthURL() {
    const url = new URL(connectors_conf["strava_oauth"]["url"]);
    for (const [param_name, param_value] of Object.entries(
        connectors_conf["strava_oauth"]["params"]
    )) {
        url.searchParams.append(param_name, param_value);
    }

    const strava_link = document.getElementById("strava_login");
    strava_link.href = url;
}

// Sets the button to get the activities from Strava
export function setGetActivitiesButton() {
    document.getElementById("get_activities").addEventListener("click", () => {
        getActivites();
    });
}

// Logins if possible to the Strava API using the client code
export function tryLoginToStrava() {
    const url = new URL(window.location.href);
    const client_code = url.searchParams.get("code");
    if (client_code) {
        loginToStrava(client_code);
        return true;
    } else {
        return false;
    }
}
