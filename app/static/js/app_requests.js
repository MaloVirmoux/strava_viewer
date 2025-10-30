/**
 * Updates the activities from the Strava API
 * @param {*} response
 */
export function updateActivities() {
    $.ajax({
        type: "PUT",
        url: "http://localhost:5000/update_activities",
        xhrFields: { withCredentials: true },
        success: () => {
            console.log("Activities imported !");
        },
    });
}
