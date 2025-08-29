document.addEventListener('DOMContentLoaded', () => {
  displayNewQuestion();
}, false);

var score = 0;
var highscore = 0;

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

async function postHighscore(score) {
  const resp = await fetch("http://localhost:8000/highscore", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({score: score})
  });

  const returnedJson = await resp.json();

  return returnedJson["game_id"];
}

async function putHighscore(game_id, score) {
  const resp = await fetch(`http://localhost:8000/highscore/${game_id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({score: score})
  });
  return await resp.json();
}

async function displayNewQuestion() {
  var question = await getRandomQuestion();
  console.log(question);

  var questionNode = document.getElementById("question")
  questionNode.innerHTML = '';
  const questionText = document.createTextNode(question["question"]);
  questionNode.appendChild(questionText);

  const answerNode = document.createElement("div");
  answers = question["wrong"];
  answers.push(question["correct"]);
  shuffleArray(answers);
  
  const correctAnswer = question["correct"];
  
  answers.forEach(answer => {
    let answerSpan = document.createElement("button");
    answerSpan.classList.add("answer");
    answerSpan.appendChild(document.createTextNode(answer));
    
    answerSpan.addEventListener('click', function() {
      checkAnswer(answer, correctAnswer, answerNode);
    });
    
    answerNode.appendChild(answerSpan);
  });
  questionNode.appendChild(answerNode);
}

function checkAnswer(selectedAnswer, correctAnswer, answerContainer) {
  const answerButtons = answerContainer.querySelectorAll('.answer');
  
  answerButtons.forEach(button => {
    const buttonText = button.textContent;
    
    if (buttonText === selectedAnswer) {
      if (selectedAnswer === correctAnswer) {
        button.classList.add('correct');
        score += 1;
      } else {
        button.classList.add('incorrect');
        score = 0;
      }
    } else if (buttonText === correctAnswer && selectedAnswer !== correctAnswer) {
      button.classList.add('show-correct');
    }
    
    button.disabled = true;
  });
  
  updateScoreDisplay();
}

async function updateScoreDisplay() {
  document.getElementById('current-score').textContent = score;

  if (score > highscore) {
    highscore = score;
    document.getElementById('highscore').textContent = highscore;

    if ("gameId" in sessionStorage) {
      await putHighscore(sessionStorage.getItem("gameId"), highscore);
    } else {
      const gameId = await postHighscore(highscore);
      sessionStorage.setItem("gameId", gameId);
    }
  }
}
