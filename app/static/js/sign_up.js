/**
 * Adds all the listeners to update the labels and submit the form
 */
function addFormListeners() {
    const password_input = document.getElementById("password_input");
    if (password_input) {
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
    }
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
