let currentQuizData = [];
let timerInterval = null;
let timeRemaining = 15 * 60;

function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

function randomizeQuizData(quizArray) {
  const shuffledQuestions = shuffleArray(quizArray);
  return shuffledQuestions.map((q) => ({
    ...q,
    options: shuffleArray([...q.options])
  }));
}

async function selectSample(filename) {
  const response = await fetch(filename);
  const blob = await response.blob();
  const file = new File([blob], filename, { type: 'application/pdf' });

  const container = new DataTransfer();
  container.items.add(file);
  document.getElementById('pdf-file').files = container.files;
}

function startTimer() {
  clearInterval(timerInterval);
  timeRemaining = 15 * 60;
  const timerBanner = document.getElementById('timer-banner');
  const timerClock = document.getElementById('timer-clock');
  
  timerBanner.style.display = 'block';

  timerInterval = setInterval(() => {
    timeRemaining--;
    
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    
    timerClock.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

    if (timeRemaining <= 0) {
      clearInterval(timerInterval);
      alert('Time is up! Submitting your quiz automatically.');
      calculateScore();
    }
  }, 1000);
}

document.getElementById('quiz-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('pdf-file');
  const errorBox = document.getElementById('error-box');
  const quizContainer = document.getElementById('quiz-container');
  const submitBtn = document.getElementById('submit-btn');
  const scoreBtn = document.getElementById('score-btn');
  const scoreBanner = document.getElementById('score-banner');
  const timerBanner = document.getElementById('timer-banner');

  if (!fileInput.files[0]) {
    alert('Please select or upload a PDF file.');
    return;
  }

  clearInterval(timerInterval);
  errorBox.style.display = 'none';
  scoreBanner.style.display = 'none';
  timerBanner.style.display = 'none';
  scoreBtn.style.display = 'none';
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
      currentQuizData = randomizeQuizData(data.quiz);
      renderQuiz(currentQuizData);
      scoreBtn.style.display = 'block';
      startTimer();
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

function renderQuiz(quiz) {
  const quizContainer = document.getElementById('quiz-container');
  quizContainer.innerHTML = '';

  quiz.forEach((q, index) => {
    const qCard = document.createElement('div');
    qCard.className = 'question-card';

    let optionsHTML = q.options.map((opt) => `
      <label class="option-label" id="label-${index}-${opt.replace(/[^a-zA-Z0-9]/g, '')}">
        <input type="radio" name="question-${index}" value="${opt}">
        ${opt}
      </label>
    `).join('');

    qCard.innerHTML = `
      <h3>Q${index + 1}. ${q.question}</h3>
      <div class="options-group">${optionsHTML}</div>
      <div class="explanation" id="exp-${index}">
        <strong>Correct Answer:</strong> ${q.answer}<br>
        <strong>Explanation:</strong> ${q.explanation}
      </div>
    `;

    quizContainer.appendChild(qCard);
  });
}

function calculateScore() {
  clearInterval(timerInterval);
  let score = 0;

  currentQuizData.forEach((q, index) => {
    const selected = document.querySelector(`input[name="question-${index}"]:checked`);
    const expDiv = document.getElementById(`exp-${index}`);
    expDiv.style.display = 'block';

    q.options.forEach((opt) => {
      const label = document.getElementById(`label-${index}-${opt.replace(/[^a-zA-Z0-9]/g, '')}`);
      if (opt === q.answer) {
        label.classList.add('correct');
      }
    });

    if (selected) {
      const selectedValue = selected.value;
      if (selectedValue === q.answer) {
        score++;
      } else {
        const selectedLabel = document.getElementById(`label-${index}-${selectedValue.replace(/[^a-zA-Z0-9]/g, '')}`);
        if (selectedLabel) selectedLabel.classList.add('incorrect');
      }
    }
  });

  const scoreBanner = document.getElementById('score-banner');
  scoreBanner.textContent = `Your Score: ${score} / ${currentQuizData.length} (${Math.round((score / currentQuizData.length) * 100)}%)`;
  scoreBanner.style.display = 'block';
  
  document.getElementById('score-btn').style.display = 'none';
  window.scrollTo({ top: scoreBanner.offsetTop - 20, behavior: 'smooth' });
}
