import { updateActivities } from "./app_requests.js";

/**
 * Adds all the listeners to make the buttons clickable
 */
function makeButtons() {
    document
        .getElementById("update-activities")
        .addEventListener("click", () => {
            updateActivities();
        });
}

makeButtons();
