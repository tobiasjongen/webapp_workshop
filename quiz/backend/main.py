import uvicorn
from fastapi import FastAPI, HTTPException
import json
import random
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# make sure to get different random numbers with each startup
random.seed(datetime.now().timestamp())

# load questions from .json file
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/questions.json', 'r') as file:
    questions = json.load(file)

highscores = dict()
highestGameId = -1

class Highscore(BaseModel):
    score: int

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/random_question")
async def randomQuestion():
    randInt = random.randint(0, len(questions)-1)
    return questions[randInt]

@app.get("/random_question/{difficulty}")
async def questionByDifficulty(difficulty):
    possibleQuestions = []
    for q in questions:
        if q['difficulty'] == int(difficulty):
            possibleQuestions.append(q)

    if len(possibleQuestions) == 0:
        raise HTTPException(
            status_code=404, 
            detail=f"no questions with difficulty {difficulty} found"
        )
    randInt = random.randint(0, len(possibleQuestions)-1)
    return possibleQuestions[randInt]

@app.get("/highscore")
async def getAllHighscores():
    global highscores
    return highscores

@app.post("/highscore")
async def storeUsrHigscore(score: Highscore):
    global highestGameId, highscores
    highestGameId = highestGameId + 1
    game_id = highestGameId    
    highscores[game_id] = score.score
    return {"game_id": game_id, "score": score.score}

@app.put("/highscore/{game_id}")
async def updateUsrHighscore(game_id: int, score: Highscore):
    global highestGameId, highscores
    if game_id > highestGameId or game_id < 0:
        raise HTTPException(status_code=404, detail="Game not found")
    highscores[game_id] = score.score
    return {"game_id": game_id, "score": score.score}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
