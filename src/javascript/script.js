import * as connectors_conf from "../conf/connectors.json";

import { loginToStrava } from "./python_api";

// Update the Strava login button URL
function setStravaOAuthURL() {
	const url = new URL(connectors_conf["strava_oauth"]["url"]);
	for (const [param_name, param_value] of Object.entries(
		connectors_conf["strava_oauth"]["params"]
	)) {
		url.searchParams.append(param_name, param_value);
	}

	const strava_link = document.getElementById("strava_login");
	strava_link.href = url;
}

setStravaOAuthURL();

// Login to the Strava API using the client code
function getClientCode() {
	const url = new URL(window.location.href);
	return url.searchParams.get("code");
}

const client_code = getClientCode();
if (client_code) {
	loginToStrava(client_code);
}
