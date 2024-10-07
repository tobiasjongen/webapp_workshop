from fastapi import FastAPI, Response, status
import json
import random
from datetime import datetime

random.seed(datetime.now().timestamp())

#load questions from .json file
with open('questions.json', 'r') as file:
    questions = json.load(file)


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/random_question")
async def randomQuestion():
    randInt = random.randint(0, len(questions)-1)
    return questions[randInt]

@app.get("/random_question/{difficulty}", status_code=200)
async def questionByDifficulty(difficulty, resp: Response):
    possibleQuestions = []
    for q in questions:
        if q['difficulty'] == int(difficulty):
            possibleQuestions.append(q)

    if len(possibleQuestions) == 0:
        resp.status_code = 500
        return {"error": f"no questions with difficulty {difficulty} found"}
    
    randInt = random.randint(0, len(possibleQuestions)-1)
    return possibleQuestions[randInt]
