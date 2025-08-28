document.addEventListener("DOMContentLoaded", () => {

  // Quiz state
  let currentQuestionIndex = 0
  let score = 0
  let showingFeedback = false

  const quizCard = document.getElementById("quiz-card")
  const progressText = document.getElementById("progress-text")
  const progressFill = document.getElementById("progress-fill")

  // Initialize the quiz
  showQuestion(currentQuestionIndex)

  // Function to display a question
  function showQuestion(index) {
    if (index >= quizData.length) {
      showResults()
      return
    }

    //Reading the data 
    const question = quizData[index]
    showingFeedback = false

    // Update progress
    progressText.textContent = `Question ${index + 1} of ${quizData.length}`
    progressFill.style.width = `${((index + 1) / quizData.length) * 100}%`

    // Create question card content
    quizCard.innerHTML = `
      <div class="question">${question.question}</div>
      <div class="options">
        ${question.options
          .map(
            (option) => `
          <div class="option" data-option="${option}">
            ${option}
          </div>
        `,
          )
          .join("")}
      </div>
    `

    // Add event listeners to options
    const options = quizCard.querySelectorAll(".option")
    options.forEach((option) => {
      option.addEventListener("click", () => {
        if (showingFeedback) return

        const selectedOption = option.dataset.option
        const isCorrect = selectedOption === question.correct_answer

        // Update score if correct
        if (isCorrect) {
          score++
        }

        // Show feedback
        showFeedback(isCorrect, question)
      })
    })
  }

  // Function to show feedback after answering
  function showFeedback(isCorrect, question) {
    showingFeedback = true

    // Create feedback card content
    quizCard.innerHTML = `
      <div class="feedback ${isCorrect ? "correct" : "incorrect"}">
        <div class="feedback-title">
          ${isCorrect ? "Correct!" : "Incorrect!"}
        </div>
        <div class="feedback-message">
          ${
            isCorrect
              ? `Yes, ${question.correct_answer} is the correct answer.`
              : `No, the correct answer is ${question.correct_answer}.`
          }
        </div>
        <p>${question.explanation}</p>
      </div>
      <button class="button next-button">Next Question</button>
    `

    // Add event listener to next button
    const nextButton = quizCard.querySelector(".next-button")
    nextButton.addEventListener("click", () => {
      currentQuestionIndex++
      showQuestion(currentQuestionIndex)
    })
  }

  // Function to show final results
  function showResults() {
    quizCard.innerHTML = `
      <div class="result-summary">
        <h2>Quiz Complete!</h2>
        <div class="score">${score}/${quizData.length}</div>
        <p>You answered ${score} out of ${quizData.length} questions correctly.</p>
        <p>Surprised by the questions and your score?</p>
        <p>Please enter the platform to explore more</p>
      </div>
      <button class="button platform-enter">Enter the Platform</button>`


    //Move to dashbaord

    const platformEnter = quizCard.querySelector(".platform-enter")
    platformEnter.addEventListener("click", function (){
      window.location.href = "/dashboard";
    })  
    // Update progress
    progressText.textContent = `Complete!`
    progressFill.style.width = "100%"
  }
})
