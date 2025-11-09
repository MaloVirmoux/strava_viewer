import { synchronizeActivitiesAPI, getTaskStatusAPI } from "./appRequests.js";

const synchronizeActivitiesButton = document.getElementById(
    "synchronize-activities"
);
const totalActivities = document.getElementById("total-activities");
let intervalSynchronizeActivitiesAPI = null;

makeButtonSynchronizeActivitiesAPI();

/**
 * Makes the button clickable to call the API
 */
function makeButtonSynchronizeActivitiesAPI() {
    synchronizeActivitiesButton.addEventListener(
        "click",
        callSynchronizeActivitiesAPI
    );
}

/**
 * Calls the API and make the button un-clickable
 */
function callSynchronizeActivitiesAPI() {
    lockButton();
    synchronizeActivitiesAPI(onSuccessSynchronizeActivitiesAPI);
}

/**
 * Calls the API to get updates from the task
 */
export function onSuccessSynchronizeActivitiesAPI(taskId) {
    lockButton();
    intervalSynchronizeActivitiesAPI = setInterval(() => {
        getTaskStatusAPI(taskId, onSuccessGetTaskStatusAPI);
    }, 1000);
}

/**
 * Gets the task status and reacts accordingly
 * @param {object} res Status of the API
 */
function onSuccessGetTaskStatusAPI(res) {
    if (res.state == "SUCCESS" || res.state == "FAILURE") {
        clearInterval(intervalSynchronizeActivitiesAPI);
        unlockButton();
        if (res.state == "SUCCESS") {
            switch (res.totalActivities) {
                case 0:
                    totalActivities.textContent = "No activity imported";
                    break;
                case 1:
                    totalActivities.textContent = "1 activity imported";
                    break;
                default:
                    totalActivities.textContent = `${res.totalActivities} activities imported`;
                    break;
            }
        }
    } else {
        synchronizeActivitiesButton.firstElementChild.textContent = res.status;
    }
}

function lockButton() {
    synchronizeActivitiesButton.classList.remove("clickable");
    synchronizeActivitiesButton.classList.add("locked");
    synchronizeActivitiesButton.removeEventListener(
        "click",
        callSynchronizeActivitiesAPI
    );
}

function unlockButton() {
    synchronizeActivitiesButton.firstElementChild.textContent =
        "Refresh the activities";
    synchronizeActivitiesButton.classList.remove("locked");
    synchronizeActivitiesButton.classList.add("clickable");
    makeButtonSynchronizeActivitiesAPI();
}
