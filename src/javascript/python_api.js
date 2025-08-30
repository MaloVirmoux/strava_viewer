export function loginToStrava(client_code) {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/login",
        data: { client_code: client_code },
        success: callbackLoginToStrava,
    });
}

function callbackLoginToStrava(response) {
    console.log(response + " is connected !");
}

export function getActivites(client_code) {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/get_activites",
        data: { client_code: client_code },
        success: callbackGetActivities,
    });
}

function callbackGetActivities(response) {
    console.log("Activities imported !");
}
