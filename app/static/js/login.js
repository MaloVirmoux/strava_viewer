/**
 * Adds the listener to toggle the visibility of the password input
 */
function makeButtons() {
    const password_input = document.getElementById("password-input");

    document
        .getElementById("show-password")
        .addEventListener("click", (event) => {
            event.target.classList.toggle("fa-eye-slash");
            const toggled_type =
                password_input.getAttribute("type") === "password"
                    ? "text"
                    : "password";
            password_input.setAttribute("type", toggled_type);
        });
}

makeButtons();
