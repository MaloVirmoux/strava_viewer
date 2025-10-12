import { login } from "./app_requests.js";

/**
 * Adds all the listeners to update the labels and submit the form
 */
function addFormListeners() {
    const password_input = document.getElementById("password_input");

    document
        .getElementById("show_password")
        .addEventListener("click", (event) => {
            event.target.classList.toggle("fa-eye-slash");
            const toggled_type =
                password_input.getAttribute("type") === "password"
                    ? "text"
                    : "password";
            password_input.setAttribute("type", toggled_type);
        });

    document
        .getElementById("login_form")
        .addEventListener("submit", (event) => {
            event.preventDefault();
            event.stopPropagation();
            submitLoginForm();
        });
}

addFormListeners();

/**
 * Submits the form
 */
function submitLoginForm() {
    const user_details = {
        email: document.getElementById("email_input").value,
        password: document.getElementById("password_input").value,
    };

    const result = login(user_details);
    if (result.status) {
        // Todo Redirect the user to the login form
    } else {
        window.alert(result.error);
    }
}
