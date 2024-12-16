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
                ui.item_label(news["title"]).classes('text-lg')
                if news["teaser"] != "":
                    ui.item_label(news["teaser"]).props('caption').classes('text-base')


with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    ui.label('Newsfeed').classes('text-bold, text-xl')

with ui.row().style('display: flex; flex-direction: row;'):
    with ui.column().style('flex: 1; margin-left: 10px;'):
        with ui.list().props('bordered separator'):
            ui.item_label('Aktuelles aus der Schule').props('header').classes('text-bold, text-xl')
            ui.separator()
            renderList(schoolNews)
    with ui.column().style('flex: 1; margin-left: 10px;'):
        with ui.list().props('bordered separator'):
            ui.item_label('Lokale Nachrichten').props('header').classes('text-bold, text-xl')
            ui.separator()
            renderList(localNews)


ui.run() #default is :8080
