import { getStravaToken, signUp } from "./app_requests.js";

/**
 * Checks if there's a client_code, verifies it, and loads form according to the result
 */
function checkClientCode() {
    const url = new URL(window.location.href);
    const client_code = url.searchParams.get("code");
    if (client_code) {
        const result = getStravaToken(client_code);
        if (result["status"]) {
            url.searchParams.set("step", 2);
            url.searchParams.set("firstname", result["firstname"]);
            url.searchParams.set("lastname", result["lastname"]);
            url.searchParams.delete("code");
            url.searchParams.delete("state");
            url.searchParams.delete("scope");
            history.pushState({}, "", url.href);
            formSteps();
        } else {
            window.alert("Uncorrect client_code from Strava\nTry to re-log in");
            window.location = window.location.pathname;
        }
    } else {
        formSteps();
    }
}

checkClientCode();

/**
 * Shows the correct inputs according to the current step
 */
function formSteps() {
    const url = new URL(window.location.href);
    const step = url.searchParams.get("step");
    switch (step) {
        case null:
        case "1":
            document.getElementById("step_1").style.display = "block";
            break;
        case "2":
            document.getElementById("step_2").style.display = "block";
            document.getElementById("firstname_input").value =
                url.searchParams.get("firstname");
            document.getElementById("lastname_input").value =
                url.searchParams.get("lastname");
            break;
    }
}

/**
 * Adds all the listeners to update the labels and submit the form
 */
function addFormListeners() {
    const password_input = document.getElementById("password_input");
    password_input.addEventListener("input", () => {
        checkPasswordStrength();
    });

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
        .getElementById("sign_up_form")
        .addEventListener("submit", (event) => {
            event.preventDefault();
            event.stopPropagation();
            submitSignUpForm();
        });
}

addFormListeners();

/**
 * Checks the strength of the password in the first field
 */
function checkPasswordStrength() {
    const password = document.getElementById("password_input").value;
    document.getElementById("password_label").innerHTML = (() => {
        if (password.length == 0) {
            return "Password";
        } else if (password.length < 8) {
            return "Use at least 8 characters";
        } else if (!/[a-z]/.test(password)) {
            return "Use at least one lowercase char";
        } else if (!/[A-Z]/.test(password)) {
            return "Use at least one uppercase char";
        } else if (!/\d/.test(password)) {
            return "Use at least one number";
        } else if (!/[@$!%*?&]/.test(password)) {
            return "Use at least one symbol (@$!%*?&)";
        } else {
            return "Valid password";
        }
    })();
}

/**
 * Submits the form
 */
function submitSignUpForm() {
    const user_details = {
        email: document.getElementById("email_input").value,
        password: document.getElementById("password_input").value,
        firstname: document.getElementById("firstname_input").value,
        lastname: document.getElementById("lastname_input").value,
    };

    const result = signUp(user_details);
    if (result.status) {
        // Todo Redirect the user to the login form
    } else {
        window.alert(result.error);
    }
}
