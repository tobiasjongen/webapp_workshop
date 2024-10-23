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


## Werkzeuge

### Frontend

#### React

NodeJS notwendig => [Installationsanleitung](https://nodejs.org/en/download/package-manager)

```bash
npx create-react-app {app-name}
cd {app-name}
npm start
```

Tipp: ChatGPT

### Backend

#### FastAPI
FastAPI => Python Package
```bash
pip install "fastapi[standard]"
```

Ausführen eines Dev-Servers:
```bash
fastapi dev main.py
```

weitere Details: siehe [FastAPI-Dokumentation](https://fastapi.tiangolo.com/)

## weitere Ideen

- Einkaufsliste
- Geburtstagskalender
- Newsfeed
    - lokale News + Schulnews + ...
    - -> Webscraping
    