/**
 * Logins to Strava using the provided client code
 * @param {String} client_code Client code provided by Strava
 */
export function getStravaToken(client_code) {
    var result;
    $.ajax({
        type: "GET",
        async: false,
        url: "http://127.0.0.1:5000/get_strava_token",
        data: { client_code: client_code },
        success: (response) => {
            result = response;
        },
        error: () => {
            result = { status: false };
        },
    });

    return result;
}

/**
 * Signs up using the provided details
 * @param {Object} user_details User details
 * @param {String} user_details.email Email of the user
 * @param {String} user_details.password Password of the user
 * @param {String} user_details.firstname First name of the user
 * @param {String} user_details.lastname Last name of the user
 */
export function signUp(user_details) {
    var result;
    $.ajax({
        type: "POST",
        async: false,
        url: "http://127.0.0.1:5000/sign_up",
        data: JSON.stringify(user_details),
        contentType: "application/json; charset=utf-8",
        success: () => {
            result = { status: true };
        },
        error: (response) => {
            result = { status: false, error: response.responseJSON.exception };
        },
    });

    return result;
}

/**
 * Logins using the provided client code
 * @param {Object} user_details User details
 * @param {String} user_details.email Email of the user
 * @param {String} user_details.password Password of the user
 */
export function login(user_details) {
    var result;
    $.ajax({
        type: "POST",
        async: false,
        url: "http://127.0.0.1:5000/login",
        data: JSON.stringify(user_details),
        contentType: "application/json; charset=utf-8",
        success: () => {
            result = { status: true };
        },
        error: (response) => {
            result = { status: false, error: response.responseJSON.exception };
        },
    });

    return result;
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
        success: () => {
            console.log("Activities imported !");
        },
    });
}
