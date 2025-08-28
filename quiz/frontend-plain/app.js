document.addEventListener('DOMContentLoaded', function() {
  displayNewQuestion();
}, false);

function shuffleArray(array) {
  for (var i = array.length - 1; i >= 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = array[i];
      array[i] = array[j];
      array[j] = temp;
  }
}

async function getRandomQuestion() {
  const resp = await fetch("http://localhost:8000/random_question");
  return await resp.json()
}

async function displayNewQuestion() {
  var question = await getRandomQuestion();
  console.log(question);

  var questionNode = document.getElementById("question")
  questionNode.innerHTML = ''; //clear old question
  const questionText = document.createTextNode(question["question"]);
  questionNode.appendChild(questionText);

  const answerNode = document.createElement("div");
  answers = question["wrong"];
  answers.push(question["correct"]);
  shuffleArray(answers);
  
  // Store the correct answer for comparison
  const correctAnswer = question["correct"];
  
  answers.forEach(answer => {
    let answerSpan = document.createElement("button");
    answerSpan.classList.add("answer");
    answerSpan.appendChild(document.createTextNode(answer));
    
    // Add click event listener to check answer
    answerSpan.addEventListener('click', function() {
      checkAnswer(answer, correctAnswer, answerNode);
    });
    
    answerNode.appendChild(answerSpan);
  });
  questionNode.appendChild(answerNode);
}

function checkAnswer(selectedAnswer, correctAnswer, answerContainer) {
  // Get all answer buttons in this container
  const answerButtons = answerContainer.querySelectorAll('.answer');
  
  answerButtons.forEach(button => {
    const buttonText = button.textContent;
    
    if (buttonText === selectedAnswer) {
      // Add class to the clicked button
      if (selectedAnswer === correctAnswer) {
        button.classList.add('correct');
      } else {
        button.classList.add('incorrect');
      }
    } else if (buttonText === correctAnswer && selectedAnswer !== correctAnswer) {
      // Add class to show correct answer border if user was wrong
      button.classList.add('show-correct');
    }
    
    // Disable all buttons after answer is selected
    button.disabled = true;
  });
}
