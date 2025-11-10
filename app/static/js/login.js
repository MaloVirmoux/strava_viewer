/**
 * Adds the listener to toggle the visibility of the password input
 */
function makeButtons() {
    const passwordInput = document.getElementById("password-input");

    document
        .getElementById("show-password")
        .addEventListener("click", (event) => {
            event.target.classList.toggle("fa-eye-slash");
            const toggledType =
                passwordInput.getAttribute("type") === "password"
                    ? "text"
                    : "password";
            passwordInput.setAttribute("type", toggledType);
        });
}

makeButtons();
