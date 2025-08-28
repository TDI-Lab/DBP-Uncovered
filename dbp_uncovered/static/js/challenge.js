document.addEventListener("DOMContentLoaded", () => {
  // Challenge state
  let currentPageIndex = 0
  let currentQuestionIndex = 0
  let pageScore = 0
  let totalScore = 0
  let showingFeedback = false
  let challengeStarted = false

  const challengeContent = document.getElementById("challenge-content")
  const progressText = document.getElementById("challenge-progress-text")
  const progressFill = document.getElementById("challenge-progress-fill")

  const totalPages = challengeData.length

  // Initialize the challenge
  showWelcomePage()

  function showWelcomePage() {
    challengeContent.innerHTML = `
            <div class="welcome-content">
                <div class="challenge-intro">
                    <h2>Mission: Escape DBP</h2>
                    <p>Your town’s water is under threat from dangerous DBPs formed during the water treatment process. 
                    You have been chosen to investigate and save town’s water supply.In order to do this you must unlock secrets behind DBPs,
                     must solve clues in each specialized room and uncover how to reduce these harmful compunds.</p>
                    
                    <div class="challenge-features">
                        <h3>What you'll learn:</h3>
                        <ul>
                            <li>DBPs and how they are formed</li>
                            <li>Types of DBPs</li>
                            <li>Health risks of DBPs</li>
                            <li>Methods for DBP reduction at home</li>
                        </ul>
                    </div>
                    
                    <div class="challenge-info">
                        <div class="info-item">
                            <strong>Duration:</strong> Approximately 5-10 minutes
                        </div>
                        <div class="info-item">
                            <strong>Format:</strong> ${totalPages} pages with 5 questions each
                        </div>
                        <div class="info-item">
                            <strong>Note:</strong> Once you start, you cannot exit until completion
                        </div>
                    </div>
                </div>
                
                <div class="challenge-actions">
                    <button class="button" id="start-challenge" style="background-color: green; color: white;">Let's Go! <br>Take me to the mission</button>
                    <button class="button" onclick="window.location.href='${dashboardUrl}'" style="background-color: red; color: white; text-decoration: none;"> I quit! <br>Not brave enough to save town</button>
                    
                </div>
            </div>
        `

    // Add event listener to start button
    document.getElementById("start-challenge").addEventListener("click", () => {
      challengeStarted = true
      showPage(currentPageIndex)
    })

    
    progressText.textContent = "Ready to start"
    progressFill.style.width = "0%"
  }

  function showPage(pageIndex) {
    if (pageIndex >= challengeData.length) {
      showCompletionPage()
      return
    }

    const page = challengeData[pageIndex]
    currentQuestionIndex = 0
    pageScore = 0
    showingFeedback = false

    // Update progress
    progressText.textContent = `Room ${pageIndex + 1} of ${challengeData.length}`
    progressFill.style.width = `${((pageIndex + 1) / challengeData.length) * 100}%`

    // Show page introduction
    showPageIntro(page)
  }

  function showPageIntro(page) {
    challengeContent.innerHTML = `
            <div class="page-intro">
                <div class="page-header">
                    <h2>${page.title}</h2>
                    <p class="page-description">${page.description}</p>
                </div>
                
                <div class="page-info">
                    <div class="info-card">
                        <h3>Learning Objectives</h3>
                        <p>In this section, you'll explore key concepts and answer questions that will help reinforce your understanding.</p>
                    </div>
                    
                    <div class="question-count">
                        <strong>Questions in this section:</strong> ${page.questions.length}
                    </div>
                </div>
                
                <button class="button" id="start-page">Begin</button>
            </div>
        `

    // Add event listener to begin section button
    document.getElementById("start-page").addEventListener("click", () => {
      showQuestion(page.questions[currentQuestionIndex])
    })
  }

  function showQuestion(question) {
    showingFeedback = false

    challengeContent.innerHTML = `
            <div class="question-content">
                <div class="question-header">
                    <div class="question-number">Question ${currentQuestionIndex + 1} of ${challengeData[currentPageIndex].questions.length}</div>
                    <div class="learning-badge">Learning Mode</div>
                </div>
                
                <div class="question-text">${question.question}</div>
                
                <div class="options">
                    ${question.options
                      .map(
                        (option, index) => `
                        <div class="option" data-option="${option}">
                            ${option}
                        </div>
                    `,
                      )
                      .join("")}
                </div>
                
                <div class="learning-content">
                    <h4>💡 Clue:</h4>
                    <p>${question.Clue}</p>
                </div>
            </div>
        `

    // Add event listeners to options
    const options = challengeContent.querySelectorAll(".option")
    options.forEach((option) => {
      option.addEventListener("click", () => {
        if (showingFeedback) return

        const selectedOption = option.dataset.option
        const isCorrect = selectedOption === question.correct_answer

        // Update score if correct
        if (isCorrect) {
          pageScore++
          totalScore++
        }

        // Show feedback
        showFeedback(isCorrect, question)
      })
    })
  }

  function showFeedback(isCorrect, question) {
    showingFeedback = true

    challengeContent.innerHTML = `
            <div class="feedback-content">
                <div class="feedback ${isCorrect ? "correct" : "incorrect"}">
                    <div class="feedback-icon">
                        ${isCorrect ? "✅" : "❌"}
                    </div>
                    <div class="feedback-title">
                        ${isCorrect ? "Excellent!" : "Not quite right"}
                    </div>
                    <div class="feedback-message">
                        ${
                          isCorrect
                            ? `Correct! ${question.correct_answer} is the right answer.`
                            : `The correct answer is: ${question.correct_answer}`
                        }
                    </div>
                </div>
                
                <div class="explanation-section">
                    <h4>📚 Explanation:</h4>
                    <p>${question.explanation}</p>
                </div>
                
                <div class="learning-reinforcement">
                    <h4>🎯 Key Takeaway:</h4>
                    <p>${question.learning_content}</p>
                </div>
                
                <button class="button" id="next-question">
                    ${
                      currentQuestionIndex < challengeData[currentPageIndex].questions.length - 1
                        ? "Next Question"
                        : "Complete"
                    }
                </button>
            </div>
        `

    // Add event listener to next button
    document.getElementById("next-question").addEventListener("click", () => {
      currentQuestionIndex++

      if (currentQuestionIndex >= challengeData[currentPageIndex].questions.length) {
        // Show page completion
        showPageCompletion()
      } else {
        // Show next question
        showQuestion(challengeData[currentPageIndex].questions[currentQuestionIndex])
      }
    })
  }

  // Show page completion
  function showPageCompletion() {
    const page = challengeData[currentPageIndex]
    const pagePercentage = Math.round((pageScore / page.questions.length) * 100)

    challengeContent.innerHTML = `
            <div class="page-completion">
                <div class="completion-header">
                    <h2>Section Complete! 🎉</h2>
                    <div class="section-score">
                        <div class="score-circle">
                            <span class="score-number">${pageScore}/${page.questions.length}</span>
                            <span class="score-label">Correct</span>
                        </div>
                    </div>
                </div>
                
                <div class="completion-summary">
                    <h3>What you learned in "${page.title}":</h3>
                    <div class="learning-summary">
                        ${page.questions
                          .map(
                            (q) => `
                            <div class="learning-point">
                                <strong>Key Concept:</strong> ${q.learning_content}
                            </div>
                        `,
                          )
                          .join("")}
                    </div>
                </div>
                
                <div class="completion-actions">
                    ${
                      currentPageIndex < challengeData.length - 1
                        ? `<button class="button" id="next-page">Continue to Next Section</button>`
                        : `<button class="button" id="finish-challenge">Complete Challenge</button>`
                    }
                </div>
            </div>
        `

    const nextButton = document.getElementById(
      currentPageIndex < challengeData.length - 1 ? "next-page" : "finish-challenge",
    )
    nextButton.addEventListener("click", () => {
      if (currentPageIndex < challengeData.length - 1) {
        currentPageIndex++
        showPage(currentPageIndex)
      } else {
        showCompletionPage()
      }
    })
  }

  // Show final completion page
  function showCompletionPage() {
    const totalQuestions = challengeData.reduce((sum, page) => sum + page.questions.length, 0)
    const finalPercentage = Math.round((totalScore / totalQuestions) * 100)

    let performanceMessage = ""
    let performanceClass = ""

    if (finalPercentage >= 90) {
      performanceMessage = "Outstanding! You've mastered the concepts! And saved the town"
      performanceClass = "excellent"
    } else if (finalPercentage >= 70) {
      performanceMessage = "Great job! You have a solid understanding of DBPs to save the town’s water supply"
      performanceClass = "good"
    } else if (finalPercentage >= 50) {
      performanceMessage = "Good effort! Consider reviewing the concepts. The town needs your support."
      performanceClass = "fair"
    } else {
      performanceMessage = "Keep learning! Practice makes perfect."
      performanceClass = "needs-improvement"
    }

    challengeContent.innerHTML = `
            <div class="challenge-completion">
                <div class="completion-celebration">
                    <div class="celebration-icon">🏆</div>
                    <h2>Challenge Complete!</h2>
                    <p class="celebration-message">Congratulations on completing the Mission DBP: Escape Room Challenge!</p>
                </div>
                
                <div class="final-results">
                    <div class="final-score ${performanceClass}">
                        <div class="score-display">
                            <span class="final-score-number">${totalScore}/${totalQuestions}</span>
                            <span class="final-percentage">${finalPercentage}%</span>
                        </div>
                        <p class="performance-message">${performanceMessage}</p>
                    </div>
                </div>
                
                <div class="learning-achievements">
                    <h3>🎓 What You've Learned:</h3>
                    <div class="achievements-grid">
                        <div class="achievement-item">
                            <div class="achievement-icon">📝</div>
                            <div class="achievement-text">DBPs and how they are formed</div>
                        </div>
                        <div class="achievement-item">
                            <div class="achievement-icon">🎨</div>
                            <div class="achievement-text">Types of DBPs</div>
                        </div>
                        <div class="achievement-item">
                            <div class="achievement-icon">⚡</div>
                            <div class="achievement-text">Health risks of DBPs</div>
                        </div>
                        <div class="achievement-item">
                            <div class="achievement-icon">🚀</div>
                            <div class="achievement-text">Methods for DBP reduction at home</div>
                        </div>
                    </div>
                </div>
                
                <div class="completion-actions">
                    <a href="${dashboardUrl}" class="button">Return to Dashboard</a>
                    <button class="button secondary" id="restart-challenge">Take Challenge Again</button>
                </div>
            </div>
        `

    // Restart functionality
    document.getElementById("restart-challenge").addEventListener("click", () => {
      currentPageIndex = 0
      currentQuestionIndex = 0
      pageScore = 0
      totalScore = 0
      challengeStarted = false
      showWelcomePage()
    })

    // Update progress
    progressText.textContent = "Challenge Complete!"
    progressFill.style.width = "100%"
    progressFill.style.backgroundColor = "#10b981"; 
  }
})
