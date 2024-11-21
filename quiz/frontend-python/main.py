from nicegui import ui
import requests
import json
import random

def check_answer(answer: str):
    if answer == response.json()["correct"]:
        ui.notify("correct")
    else:
        ui.notify("false")


response = requests.get("http://localhost:8000/random_question")
answers = response.json()["wrong"]
answers.append(response.json()["correct"])
random.shuffle(answers)

ui.label(response.json()["question"])

with ui.row():
    for answer in answers:
        ui.button(answer, on_click=check_answer(answer))


#ui.label('Hello NiceGUI!')

ui.run() #default is :8080