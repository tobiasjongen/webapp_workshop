# smallWebserverExamples
Einige kleine Beispiele für Webanwendugen, die im Rahmen eines Wochenend-Workshops von Schülern entwickelt werden könnten.

## Beispiele

### Quiz

Im Ordner [/quiz](./quiz) befindet sich eine simple Quiz-Anwendung, die sich aus einem Frontend und einem Backend zusammensetzt.

#### Mögliche Erweiterungsideen:

- Schwierigkeit der Fragen basierend auf Anzahl der richtigen Antworten generieren
- "Joker" hinzufügen
- falsche Antworten zu Fragen zufällig generieren (per LLM (z. B. chatGPT))
- Fragen in einer Datenbank speichern
- Highscore als Cookie im Browser speichern
- Nutzer-System bauen  
    - Login 
    - Highscore pro Nutzer
    - Scoreboard

### Newsfeed

Im Ordner [/newsfeed](./newsfeed/) befindet sich eine einfache Newsfeed-Anwendung. Diese sammelt aktuelle Nachrichten aus dem Web und stellt sie dar.

- lokale News + Schulnews + ...

#### Mögliche Erweiterungsideen:

- caching: 
    - nicht bei jeder Anfrage neues Scraping durchführen, sondern Ergbnisse zwischenspeichern, nach bestimmter Zeit ablaufen lassen
    - Scraping in weiteren Dienst auslagern, der automatisch von Zeit zu Zeit vom Backend angefragt wird, damit es zu keinen Zeitverzögerungen kommt
    - schönere Teaser-Texte anzeigen -> Links folgen -> Achtung: nicht zu viel Last auf Server, sonst ggf. von Server auf Blacklist gesetzt
- Filtern nach Schlüsselworten in den Neuigkeiten

### weitere Ideen für Anwendungen

- Einkaufsliste
- Geburtstagskalender
    

## Werkzeuge

### venv

Um die für ein Projekt benötigten Python-Pakete zu installieren, kann eine virtuelle Umgebung (`venv`) verwendet werden. Dadurch werden die Pakete nicht lokal installiert. Dies kann insbesondere dann hilfreich sein, wenn für verschiedene Projekte das gleiche Paket in unterschiedlichen Versionen notwendig ist. 

```bash
pip install virtualenv
cd {project}
python3 -m venv env
source myvenv/bin/activate #linux, mac; windows: 'venv\Scripts\activate.bat' oder 'venv\Scripts\Activate.ps1'
pip install -r requirements.txt
```

Hinweis: Für jede neue Terminal-Session muss die Umgebung neu aktiviert werden (`source myvenv/bin/activate`).

### Frontend

#### kein Framework/Library: HTML, CSS, JS

TBA

#### Python NiceGUI

NiceGUI => Python Package

Ausführen:
```bash
python3 main.py
```

weitere Detauls: siehe [Dokumentation](https://nicegui.io/documentation)

#### React

- kann sehr viel
- für einfache Anwendung vermutlich zu komplex (wie solche, die im Rahmen einen Wochenend-Workshops entwickelt werden)

NodeJS notwendig => [Installationsanleitung](https://nodejs.org/en/download/package-manager)

```bash
npx create-react-app {app-name}
cd {app-name}
npm start
```

Tipp: ChatGPT ist im Generieren von einfach React-Frontends recht gut. 

### Backend

#### FastAPI
FastAPI ist eine Python-Bibliothek, die für die komfortable Erstellung eines Backends beziehungsweise einer API bentuzt werden kann.

Ausführen eines Dev-Servers:
```bash
fastapi dev main.py
```

weitere Details: siehe [FastAPI-Dokumentation](https://fastapi.tiangolo.com/)

#### Beautiful Soup
Beautiful Soup ist eine Python-Bibliothek, die das Web-Scraping vereinfacht. Sie bietet die Möglichkeit, komfortabel Informationen aus HTML-Dokumenten zu parsen. 

[Dokumenation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
