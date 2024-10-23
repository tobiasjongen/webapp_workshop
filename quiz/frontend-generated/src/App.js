// This code was generated with ChatGPT.

import React, { useState, useEffect } from 'react';
import './App.css';

// Fisher-Yates shuffle algorithm to randomize answers
function shuffleArray(array) {
  let shuffledArray = [...array]; // Create a copy to avoid mutating the original array
  for (let i = shuffledArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
  }
  return shuffledArray;
}

function App() {
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [shuffledAnswers, setShuffledAnswers] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [isCorrect, setIsCorrect] = useState(null); // To track if the answer is correct
  const [answerChecked, setAnswerChecked] = useState(false);
  const [loading, setLoading] = useState(true); // For loading state

  // Function to fetch a question from the backend
  const fetchQuestion = async () => {
    try {
      setLoading(true); // Set loading state to true while fetching
      const response = await fetch('http://localhost:8000/random_question');
      const data = await response.json();
      setCurrentQuestion(data);
      let answers = []
      answers.push(data.correct)
      for (let i = 0; i < data.wrong.length; i++) {
        answers.push(data.wrong[i])
      }
      setShuffledAnswers(shuffleArray(answers));
    } catch (error) {
      console.error("Error fetching question:", error);
    } finally {
      setLoading(false); // Set loading state to false after fetching
    }
  };

  // Fetch a new question when the component mounts and for each new question
  useEffect(() => {
    fetchQuestion();
  }, []);

  // Handle answer selection
  const handleAnswerClick = (index) => {
    if (answerChecked) return; // Prevent further clicks after an answer is chosen

    setSelectedAnswer(index);
    console.log(shuffledAnswers[index] + " " + currentQuestion.correct);
    setIsCorrect(shuffledAnswers[index] === currentQuestion.correct);
    setAnswerChecked(true);

    // Automatically fetch a new question after 3 seconds
    setTimeout(() => {
      fetchQuestion();
      setSelectedAnswer(null); // Reset selected answer
      setIsCorrect(null); // Reset correctness
      setAnswerChecked(false); // Allow new answer selection
    }, 3000);
  };

  if (loading) {
    return <div className="App">Loading...</div>; // Display loading state while fetching
  }

  return (
    <div className="App">
      <h1>Question Quiz</h1>
      <div className="question-box">
        <h2>{currentQuestion.question}</h2>
        <div className="answers">
          {shuffledAnswers.map((answerObj, index) => (
            <button
              key={index}
              className={`answer-button ${
                answerChecked
                  ? index === selectedAnswer
                    ? isCorrect
                      ? "correct"
                      : "wrong"
                    : ""
                  : ""
              }`}
              onClick={() => handleAnswerClick(index)}
              disabled={answerChecked} // Disable buttons after an answer is checked
            >
              {answerObj}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
