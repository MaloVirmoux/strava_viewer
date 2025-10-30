/**
 * Updates the activities from the Strava API
 */
export function synchronizeActivitiesAPI(func) {
    $.ajax({
        type: "PUT",
        url: "http://localhost:5000/synchronize_activities",
        xhrFields: { withCredentials: true },
        success: (task_id) => {
            func(task_id);
        },
    });
}

/**
 * Gets the status of the provided task
 * @param {string} task_id ID of the task
 * @param {function} func Function to call on success
 */
export function getTaskStatusAPI(task_id, func) {
    $.ajax({
        type: "GET",
        url: `http://localhost:5000/task_status/${task_id}`,
        xhrFields: { withCredentials: true },
        success: (res) => {
            func(res);
        },
    });
}
