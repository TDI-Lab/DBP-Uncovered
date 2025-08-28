document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm")
  const usernameInput = document.getElementById("username")
  const passwordInput = document.getElementById("password")
  const confirmPasswordInput = document.getElementById("confirmPassword")
  const submitButton = document.getElementById("submitButton")
  const errorContainer = document.getElementById("errorContainer")
  const loadingSpinner = document.getElementById("loadingSpinner")

  // Real-time validation functions
  function validateUsername() {
    const username = usernameInput.value.trim()
    const usernameError = document.getElementById("usernameError")

    if (username.length === 0) {
      usernameError.textContent = ""
      usernameInput.classList.remove("error")
      return false
    } else if (username.length < 3) {
      usernameError.textContent = "Username must be at least 3 characters long"
      usernameInput.classList.add("error")
      return false
    } else if (username.length > 100) {
      usernameError.textContent = "Username must be less than 100 characters"
      usernameInput.classList.add("error")
      return false
    } else {
      usernameError.textContent = ""
      usernameInput.classList.remove("error")
      return true
    }
  }

  function validatePassword() {
    const password = passwordInput.value
    const passwordError = document.getElementById("passwordError")
    const strengthIndicator = document.getElementById("passwordStrength")
    const strengthFill = document.getElementById("strengthFill")

    if (password.length === 0) {
      passwordError.textContent = ""
      strengthIndicator.textContent = ""
      strengthIndicator.className = "password-strength"
      strengthFill.style.width = "0%"
      passwordInput.classList.remove("error")
      return false
    } else if (password.length < 6) {
      passwordError.textContent = "Password must be at least 6 characters long"
      strengthIndicator.textContent = "Too short"
      strengthIndicator.className = "password-strength weak"
      strengthFill.style.width = "20%"
      strengthFill.style.backgroundColor = "#e74c3c"
      passwordInput.classList.add("error")
      return false
    } else {
      passwordError.textContent = ""
      passwordInput.classList.remove("error")

      // Calculate password strength
      let strength = 0
      if (password.length >= 8) strength++
      if (/[A-Z]/.test(password)) strength++
      if (/[a-z]/.test(password)) strength++
      if (/[0-9]/.test(password)) strength++
      if (/[^A-Za-z0-9]/.test(password)) strength++

      if (strength <= 2) {
        strengthIndicator.textContent = "Weak"
        strengthIndicator.className = "password-strength weak"
        strengthFill.style.width = "40%"
        strengthFill.style.backgroundColor = "#e74c3c"
      } else if (strength <= 3) {
        strengthIndicator.textContent = "Medium"
        strengthIndicator.className = "password-strength medium"
        strengthFill.style.width = "70%"
        strengthFill.style.backgroundColor = "#f39c12"
      } else {
        strengthIndicator.textContent = "Strong"
        strengthIndicator.className = "password-strength strong"
        strengthFill.style.width = "100%"
        strengthFill.style.backgroundColor = "#27ae60"
      }

      return true
    }
  }

  function validateConfirmPassword() {
    const password = passwordInput.value
    const confirmPassword = confirmPasswordInput.value
    const confirmError = document.getElementById("confirmPasswordError")

    if (confirmPassword.length === 0) {
      confirmError.textContent = ""
      confirmPasswordInput.classList.remove("error")
      return false
    } else if (password !== confirmPassword) {
      confirmError.textContent = "Passwords do not match"
      confirmPasswordInput.classList.add("error")
      return false
    } else {
      confirmError.textContent = ""
      confirmPasswordInput.classList.remove("error")
      return true
    }
  }

  function updateSubmitButton() {
    const isValid = validateUsername() && validatePassword() && validateConfirmPassword()
    submitButton.disabled = !isValid
  }

  // Event listeners for real-time validation
  usernameInput.addEventListener("input", () => {
    validateUsername()
    updateSubmitButton()
  })

  passwordInput.addEventListener("input", () => {
    validatePassword()
    validateConfirmPassword() // Re-validate confirm password when password changes
    updateSubmitButton()
  })

  confirmPasswordInput.addEventListener("input", () => {
    validateConfirmPassword()
    updateSubmitButton()
  })

  function showErrors(errors) {
    errorContainer.innerHTML = ""
    if (errors && errors.length > 0) {
      const errorList = document.createElement("ul")
      errorList.className = "error-list"

      errors.forEach((error) => {
        const errorItem = document.createElement("li")
        errorItem.textContent = error
        errorList.appendChild(errorItem)
      })

      errorContainer.appendChild(errorList)
      errorContainer.style.display = "block"
    } else {
      errorContainer.style.display = "none"
    }
  }

  function showLoading(show) {
    if (show) {
      loadingSpinner.style.display = "block"
      submitButton.disabled = true
      submitButton.querySelector(".btn-text").textContent = "Creating Account..."
    } else {
      loadingSpinner.style.display = "none"
      submitButton.disabled = false
      submitButton.querySelector(".btn-text").textContent = "Create Account"
    }
  }

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault()

    // Final validation
    if (!validateUsername() || !validatePassword() || !validateConfirmPassword()) {
      showErrors(["Please fix the validation errors above."])
      return
    }

    showLoading(true)
    showErrors([])

    const formData = {
      username: usernameInput.value.trim(),
      password: passwordInput.value,
      confirm_password: confirmPasswordInput.value,
    }

    try {
      const response = await fetch("/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })

      const data = await response.json()

      if (data.status === "success") {
        // Show success message briefly before redirect
        submitButton.querySelector(".btn-text").textContent = "Success! Redirecting..."
        submitButton.className = "submit-btn success"

        setTimeout(() => {
          window.location.href = data.redirect_url
        }, 1000)
      } else if (data.status === "error") {
        showErrors(data.errors || ["Registration failed. Please try again."])
      }
    } catch (error) {
      console.error("Registration error:", error)
      showErrors(["Network error. Please check your connection and try again."])
    } finally {
      showLoading(false)
    }
  })

  // Initial validation state
  updateSubmitButton()
})
