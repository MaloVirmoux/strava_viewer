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
}

addFormListeners();
