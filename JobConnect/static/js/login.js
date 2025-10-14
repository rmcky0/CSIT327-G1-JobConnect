document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form"); 

    const usernameField = document.querySelector("#id_username"); 
    const passwordField = document.querySelector("#id_password");
    
    const errors = {
        username: document.querySelector("#username-error"),
        password: document.querySelector("#password-error"),
    };

    function validateUsername() {
        const value = usernameField.value.trim();
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (value === "") {
            errors.username.textContent = "Email address is required.";
            return false;
        }
        
        if (!pattern.test(value)) {
            errors.username.textContent = "Enter a valid email address.";
            return false;
        }
        
        errors.username.textContent = "";
        return true;
    }

    function validatePassword() {
        const value = passwordField.value;
        
        if (value.length === 0) {
            errors.password.textContent = "Password is required.";
            return false;
        }

        errors.password.textContent = "";
        return true;
    }

    if (usernameField) {
        usernameField.addEventListener("input", validateUsername);
    }
    
    if (passwordField) {
        passwordField.addEventListener("input", validatePassword);
    }
    
    document.querySelectorAll(".password-toggle").forEach(toggle => {
        toggle.addEventListener("click", function () {
            const input = this.previousElementSibling; 
            
            if (input.type === "password") {
                input.type = "text";
                this.classList.replace("fa-eye", "fa-eye-slash"); 
            } else {
                input.type = "password";
                this.classList.replace("fa-eye-slash", "fa-eye");
            }
        });
    });

    
    if (form) {
        form.addEventListener("submit", function (e) {
            const isUsernameValid = validateUsername();
            const isPasswordValid = validatePassword();

            const formValid = isUsernameValid && isPasswordValid;

            if (!formValid) {
                e.preventDefault();
            }
        });
    }
});