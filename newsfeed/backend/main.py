import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests import get
from bs4 import BeautifulSoup
import re
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cached results and timestamps
schoolNews = []
timestampSchool = datetime.datetime.now()
localNews = []
timestampLocal = datetime.datetime.now()
CACHE_EXPIRATION_TIME = 60*5

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/local")
async def getLocalNews():
    global localNews, timestampLocal
    if (not localNews or (datetime.datetime.now() - timestampLocal).total_seconds() > CACHE_EXPIRATION_TIME):
        print("fetching latest local news...")

        localNews = []
        timestampLocal = datetime.datetime.now()
        url = 'https://www.medienservice.sachsen.de/medien/rmi/press_releases.json?count=15'
        response = get(url)
        contentJson = response.json()

        for article in contentJson['press_releases']:
            entry = {}
            entry['link'] = article['url']
            entry['title'] = article['title']
            content_plain = article['content-plain']
            if len(content_plain) > 300:
                shortenedTeaser = content_plain[:300] + "..."
            else:
                shortenedTeaser = content_plain
            entry['teaser'] = re.sub(r"\s+", " ", shortenedTeaser)
            
            localNews.append(entry)

    return localNews

@app.get("/school")
async def getSchoolNews():
    global schoolNews, timestampSchool
    if (not schoolNews or (datetime.datetime.now() - timestampSchool).total_seconds() > CACHE_EXPIRATION_TIME):
        print("crawling latest school news...")

        url = 'https://www.franziskaneum.de/wp/category/aktuelles/'
        response = get(url)
        timestampSchool = datetime.datetime.now()
        html_soup = BeautifulSoup(response.text, 'html.parser')
        schoolNews = []

        for article in html_soup.find_all('article', class_='post'):
            entry = {}
            title =  article.find(class_='entry-title')
            link = article.find(class_='entry-title').find('a')
            teaser = article.find(class_='entry-summary').find('p')
            
            if title == None or link == None: # skip invalid occurences
                continue

            teaser = re.sub('([\t\n\\\/]+|(Weiterlesen))', ' ', teaser.get_text()) #replace unwanted stuff with whitespaces
            teaser = re.sub('[\s]+', ' ', teaser) #remove multiple whitespaces
            entry["title"] = title.get_text().strip() # strip() removes leading and trailing whitespaces
            entry["link"] = link.get('href')
            entry["teaser"] = teaser.strip() if teaser is not None else ""
            schoolNews.append(entry)

    return schoolNews

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
