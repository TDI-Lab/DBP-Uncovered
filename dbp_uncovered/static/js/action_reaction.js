document.addEventListener("DOMContentLoaded", () => {
  // Quiz state
  let currentQuestionIndex = 0;
  const userAnswers = [];

  const quizCard = document.getElementById("quiz-card");
  const likert = document.getElementById("likert");
  const progressText = document.getElementById("progress-text");
  const progressFill = document.getElementById("progress-fill");

  const likerQuestions = ["Time", "Cost", "Frequency", "Effectiveness"];

  // Initialize the quiz
  showQuestion(currentQuestionIndex);

  // Function to display a question
  function showQuestion(index) {
    const question = quizData[index];

    // Update progress
    progressText.textContent = `Question ${index + 1} of ${quizData.length}`;
    progressFill.style.width = `${((index + 1) / quizData.length) * 100}%`;

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
        `
          )
          .join("")}
      </div>
    `;

    // Add event listeners to options
    const options = quizCard.querySelectorAll(".option");
    options.forEach((option) => {
      option.addEventListener("click", () => {
        const selectedOption = option.dataset.option;

        // Save answers
        userAnswers.push({
          id: question.id,
          question: question.question,
          selected: selectedOption,
          type: "quiz",
        });

        if (currentQuestionIndex === quizData.length - 1) {
          showPreferenceForm(); // Call async wrapper
        } else {
          currentQuestionIndex++;
          showQuestion(currentQuestionIndex);
        }
      });
    });
  }

  // Async wrapper to show preference form and handle submit
  async function showPreferenceForm() {
    quizCard.style.display = "none";

    let likertHtml = `
      <h2> Set Your Preference</h2>
      <br>
      <p style="text-align: center;"> Score each factor 1–5. Higher means you can invest more time/cost/frequency or you want stronger effectiveness from the actions to reduce DBPs. Your ratings shape the action list tailored to you.</p>`;
    likerQuestions.forEach((question, index) => {
      likertHtml += `
        <div class="likert-block">
          <p>${question}</p>
          <div class="likert-scale" data-question="${index}">
            <label><input type="radio" name="likert-${index}" value="1"><span>1</span></label>
            <label><input type="radio" name="likert-${index}" value="2"><span>2</span></label>
            <label><input type="radio" name="likert-${index}" value="3"><span>3</span></label>
            <label><input type="radio" name="likert-${index}" value="4"><span>4</span></label>
            <label><input type="radio" name="likert-${index}" value="5"><span>5</span></label>
          </div>
        </div>
      `;
    });

    likertHtml += `
      <button id="submit-preference" class="button submit-button">Submit</button>
    `;

    likert.innerHTML = likertHtml;
    likert.style.display = "block";

    document
      .getElementById("submit-preference")
      .addEventListener("click", async () => {
        likerQuestions.forEach((q, index) => {
          const selected = document.querySelector(
            `input[name="likert-${index}"]:checked`
          );
          if (selected) {
            userAnswers.push({
              question: q,
              selected: selected.value,
              type: "preference",
            });
          }
        });

        try {
          const resp = await fetch("/action_reaction", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers: userAnswers }),
          });

          if (!resp.ok) {
            console.error("Server error:", resp.status, await resp.text());
            return;
          }

          const payload = await resp.json();
          if (payload.status === "success" && payload.redirect_url) {
            window.location.href = payload.redirect_url;
          } else {
            console.error("Unexpected response payload:", payload);
          }
        } catch (err) {
          console.error("Fetch failed:", err);
        }
      });
  }
});
