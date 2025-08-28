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

'''CORS policy'''
# Define the origins that should be allowed to make CORS requests
origins = [
    "http://localhost:8080",
]

# Add CORS middleware to FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
highestUsrId = -1

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

@app.get("/highscore/{usr_id}")
async def getUsrHighscore(usr_id: int):
    global highestUsrId, highscores
    if usr_id > highestUsrId or usr_id < 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": usr_id, "score": highscores[usr_id]}

@app.get("/highscore")
async def getAllHighscores():
    global highscores
    return highscores

@app.post("/highscore")
async def storeUsrHigscore(score: Highscore):
    global highestUsrId, highscores
    highestUsrId = highestUsrId + 1
    usr_id = highestUsrId    
    highscores[usr_id] = score.score
    return {"user_id": usr_id, "score": score.score}

@app.put("/highscore/{usr_id}")
async def updateUsrHighscore(usr_id: int, score: Highscore):
    global highestUsrId, highscores
    if usr_id > highestUsrId or usr_id < 0:
        raise HTTPException(status_code=404, detail="User not found")
    highscores[usr_id] = score.score
    return {"user_id": usr_id, "score": score.score}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
