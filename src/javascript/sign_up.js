import { passwordStrength } from "check-password-strength";

/**
 * Adds all the listeners to update the labels and submit the form
 */
function addFormListeners() {
    document
        .getElementById("password_input_1")
        .addEventListener("input", () => {
            checkPasswordStrength();
            checkIdenticalPassword();
        });
    document
        .getElementById("password_input_2")
        .addEventListener("input", checkIdenticalPassword);

    document
        .getElementById("sign_up_form")
        .addEventListener("submit", (event) => {
            event.preventDefault();
            event.stopPropagation();
            console.log("Form submitted");
            submitSignUpForm();
        });
}

addFormListeners();

/**
 * Checks the strength of the password in the first field
 */
function checkPasswordStrength() {
    const password = document.getElementById("password_input_1").value;
    const strength = passwordStrength(password).id;
    document.getElementById("password_label_1").innerHTML = (() => {
        if (password.length == 0) {
            return "Password";
        } else {
            return "Password (strength : " + strength + "/3)";
        }
    })();
}

/**
 * Checks if the passwords are identical in both fields
 */
function checkIdenticalPassword() {
    const password_1 = document.getElementById("password_input_1").value;
    const password_2 = document.getElementById("password_input_2").value;
    document.getElementById("password_label_2").innerHTML = (() => {
        if (password_2.length == 0) {
            return "Repeat your password";
        } else if (password_1 == password_2) {
            return "Identical password entered";
        } else {
            return "Passwords are different !";
        }
    })();
}

/**
 * Does the checks and submits the form
 */
function submitSignUpForm() {
    const email = document.getElementById("email_input").value;
    const password_1 = document.getElementById("password_input_1").value;
    const password_2 = document.getElementById("password_input_2").value;
    const firstname = document.getElementById("firstname_input").value;
    const lastname = document.getElementById("lastname_input").value;

    if (password_1 !== password_2) {
        window.alert("Passwords aren't identical");
    }

    window.alert(passwordStrength(password_1).value);
}
