// Fisher-Yates Shuffle Algorithm for arrays
function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// Function to shuffle question order and their individual choices
function randomizeQuizData(quizArray) {
  const shuffledQuestions = shuffleArray(quizArray);
  return shuffledQuestions.map((q) => ({
    ...q,
    options: shuffleArray([...q.options])
  }));
}

// Helper to select sample PDFs directly into input
async function selectSample(filename) {
  const response = await fetch(filename);
  const blob = await response.blob();
  const file = new File([blob], filename, { type: 'application/pdf' });

  const container = new DataTransfer();
  container.items.add(file);
  document.getElementById('pdf-file').files = container.files;
}

// Form Submission & API Trigger
document.getElementById('quiz-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('pdf-file');
  const errorBox = document.getElementById('error-box');
  const quizContainer = document.getElementById('quiz-container');
  const submitBtn = document.getElementById('submit-btn');

  if (!fileInput.files[0]) {
    alert('Please select or upload a PDF file.');
    return;
  }

  errorBox.style.display = 'none';
  quizContainer.innerHTML = '';
  submitBtn.disabled = true;
  submitBtn.textContent = 'Generating Quiz...';

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('num_questions', 20);

  try {
    const response = await fetch('https://pdf-quiz-generator-b35g.onrender.com/api/generate-quiz', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (data.status === 'success' && data.quiz) {
      const randomizedQuiz = randomizeQuizData(data.quiz);
      renderQuiz(randomizedQuiz);
    } else {
      throw new Error(data.message || 'Failed to generate quiz.');
    }
  } catch (err) {
    errorBox.textContent = `Error: ${err.message}`;
    errorBox.style.display = 'block';
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Generate 20-Question Quiz';
  }
});

// Render Quiz Questions on UI
function renderQuiz(quiz) {
  const quizContainer = document.getElementById('quiz-container');
  quizContainer.innerHTML = '';

  quiz.forEach((q, index) => {
    const qCard = document.createElement('div');
    qCard.className = 'question-card';

    let optionsHTML = q.options.map((opt) => `
      <label class="option-label">
        <input type="radio" name="question-${index}" value="${opt}">
        ${opt}
      </label>
    `).join('');

    qCard.innerHTML = `
      <h3>Q${index + 1}. ${q.question}</h3>
      <div class="options-group">${optionsHTML}</div>
      <div class="explanation" id="exp-${index}">
        <strong>Answer:</strong> ${q.answer}<br>
        <strong>Explanation:</strong> ${q.explanation}
      </div>
    `;

    quizContainer.appendChild(qCard);
  });
}