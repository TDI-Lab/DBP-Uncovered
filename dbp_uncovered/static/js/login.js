document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm")
  const usernameInput = document.getElementById("username")
  const passwordInput = document.getElementById("password")
  const submitBtn = document.getElementById("submitBtn")

  // Error display elements
  const usernameError = document.getElementById("username-error")
  const passwordError = document.getElementById("password-error")
  const formErrors = document.getElementById("form-errors")
  const errorList = document.getElementById("error-list")

  // Validation state
  const validationState = {
    username: false,
    password: false,
  }

  // Username validation
  usernameInput.addEventListener("input", function () {
    const username = this.value.trim()
    const usernameGroup = this.closest(".form-group")

    if (username.length === 0) {
      showFieldError(usernameError, "")
      this.className = ""
      validationState.username = false
    } else {
      showFieldError(usernameError, "")
      this.className = ""
      validationState.username = true
    }

    updateSubmitButton()
  })

  // Password validation
  passwordInput.addEventListener("input", function () {
    const password = this.value
    const passwordGroup = this.closest(".form-group")

    if (password.length === 0) {
      showFieldError(passwordError, "")
      this.className = ""
      validationState.password = false
    } else {
      showFieldError(passwordError, "")
      this.className = ""
      validationState.password = true
    }

    updateSubmitButton()
  })

  function showFieldError(errorElement, message) {
    errorElement.textContent = message
  }

  function updateSubmitButton() {
    const isValid = validationState.username && validationState.password
    submitBtn.disabled = !isValid
  }

  function showFormErrors(errors) {
    errorList.innerHTML = ""
    errors.forEach((error) => {
      const li = document.createElement("li")
      li.textContent = error
      errorList.appendChild(li)
    })
    formErrors.style.display = "block"
    formErrors.scrollIntoView({ behavior: "smooth", block: "nearest" })
  }

  function hideFormErrors() {
    formErrors.style.display = "none"
  }

  function setLoadingState(loading) {
    const btnText = submitBtn.querySelector(".btn-text")
    const loadingSpinner = submitBtn.querySelector(".loading-spinner")

    if (loading) {
      submitBtn.classList.add("loading")
      submitBtn.disabled = true
      btnText.style.opacity = "0"
      loadingSpinner.style.display = "block"
    } else {
      submitBtn.classList.remove("loading")
      submitBtn.disabled = !Object.values(validationState).every(Boolean)
      btnText.style.opacity = "1"
      loadingSpinner.style.display = "none"
    }
  }

  // Form submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault()

    hideFormErrors()
    setLoadingState(true)

    const formData = {
      username: usernameInput.value.trim(),
      password: passwordInput.value,
    }

    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })

      const result = await response.json()

      if (result.status === "success") {
        // Success - redirect to results
        window.location.href = result.redirect_url
      } else if (result.status === "error") {
        // Show errors
        showFormErrors(result.errors)
        setLoadingState(false)
      }
    } catch (error) {
      console.error("Login error:", error)
      showFormErrors(["An unexpected error occurred. Please try again."])
      setLoadingState(false)
    }
  })

  // Initialize
  updateSubmitButton()
})
