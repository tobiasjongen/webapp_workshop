from nicegui import ui
import requests
import random

def check_answer(answer: str, btn: ui.button, correct_answer: str):
    if answer == correct_answer:
        ui.notify("richtig", position="top")
        btn.style('background-color: green !important;') #!important to override default color
    else:
        ui.notify("falsch", position="top")
        btn.style('background-color: red !important;')


@ui.refreshable
def init_question():
    response = requests.get("http://localhost:8000/random_question")
    answers = response.json()["wrong"]
    answers.append(response.json()["correct"])
    random.shuffle(answers)
    correct_answer = response.json()["correct"]
    container = ui.column().classes('border p-4') \
        .style('position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);')

    with container:
        with ui.row().style('margin: auto;'):
            ui.label(response.json()["question"]).style('text-align: center;').classes("text-xl")
        with ui.row().style('margin: auto;'):
            for answer in answers:
                btn = ui.button(answer)
                btn.on_click(lambda a=answer,b=btn: check_answer(a,b, correct_answer))
        with ui.row().style('margin: auto;'):
            ui.button("Nächste Frage").on_click(init_question.refresh)


init_question()

ui.run() #default is :8080
# run app with 'python main.py'