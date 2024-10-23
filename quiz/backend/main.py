from fastapi import FastAPI, Response, status
import json
import random
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

'''CORS policy'''
# Define the origins that should be allowed to make CORS requests
origins = [
    "http://localhost:3000",  # React frontend
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
with open('questions.json', 'r') as file:
    questions = json.load(file)


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
