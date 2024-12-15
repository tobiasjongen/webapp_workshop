from nicegui import ui
import requests


localNews : dict = requests.get("http://localhost:8000/local").json()
schoolNews : dict = requests.get("http://localhost:8000/school").json()

def readMore(link: str):
    ui.navigate.to(link, new_tab=True)

def renderList(newsJson : dict):
    for news in newsJson:
        with ui.item(on_click=lambda link=news["link"]: readMore(link)):
            with ui.item_section():
                ui.item_label(news["title"])
                ui.item_label(news["teaser"]).props('caption')
            with ui.item_section().props('side'):
                ui.icon('read_more')


with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    ui.label('Newsfeed')

with ui.row().style('display: flex; flex-direction: row;'):
    with ui.column().style('flex: 1; margin-left: 10px;'):
        with ui.list().props('bordered separator'):
            ui.item_label('Neuigkeiten aus der Schule').props('header').classes('text-bold')
            ui.separator()
            renderList(schoolNews)
    with ui.column().style('flex: 1; margin-left: 10px;'):
        with ui.list().props('bordered separator'):
            ui.item_label('Lokale Neuigkeiten').props('header').classes('text-bold')
            ui.separator()
            renderList(localNews)


ui.run() #default is :8080
