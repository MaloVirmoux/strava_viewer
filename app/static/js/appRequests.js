/**
 * Updates the activities from the Strava API
 */
export function synchronizeActivitiesAPI(func) {
    $.ajax({
        type: "PUT",
        url: "http://localhost:5000/synchronize_activities",
        xhrFields: { withCredentials: true },
        success: (taskId) => {
            func(taskId);
        },
    });
}

/**
 * Gets the status of the provided task
 * @param {string} taskId ID of the task
 * @param {function} func Function to call on success
 */
export function getTaskStatusAPI(taskId, func) {
    $.ajax({
        type: "GET",
        url: `http://localhost:5000/task_status/${taskId}`,
        xhrFields: { withCredentials: true },
        success: (res) => {
            func(res);
        },
    });
}
