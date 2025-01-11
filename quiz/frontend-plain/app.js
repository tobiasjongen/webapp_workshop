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
  answers.forEach(answer => {
    let answerSpan = document.createElement("button");
    answerSpan.classList.add("answer");
    answerSpan.appendChild(document.createTextNode(answer));
    answerNode.appendChild(answerSpan);
  });
  questionNode.appendChild(answerNode);
}
