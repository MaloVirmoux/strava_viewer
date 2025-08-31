/**
 * Logins to Strava using the provided client code
 * @param {String} client_code Client code provided by Strava
 */
export function loginToStrava(client_code) {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/login",
        data: { client_code: client_code },
        success: callbackLoginToStrava,
    });
}

/**
 * Callback from the login backend
 * @param {*} response
 */
function callbackLoginToStrava(response) {
    console.log(response + " is connected !");
}

/**
 * Gets the activities from the Strava API
 * @param {*} response
 */
export function getActivites(client_code) {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/get_activites",
        data: { client_code: client_code },
        success: callbackGetActivities,
    });
}

/**
 * Callback from the activities backend
 * @param {*} response
 */
function callbackGetActivities(response) {
    console.log("Activities imported !");
}
