from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests import get
from bs4 import BeautifulSoup
import re
import datetime

app = FastAPI()

'''CORS policy'''
# Define the origins that should be allowed to make CORS requests
origins = [
    "http://localhost:8080"
]

# Add CORS middleware to FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##cached results and timestamps
schoolNews = []
timestampSchool = datetime.datetime.now()
localNews = []
timestampLocal = datetime.datetime.now()
cacheExpirationTime = 60*5

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/local")
async def getLocalNews():
    global localNews, timestampLocal
    if (not localNews or (datetime.datetime.now() - timestampLocal).total_seconds() > cacheExpirationTime):
        print("crawling latest data...")

        url = 'https://www.saechsische.de/lokales/meissen-lk/'
        response = get(url)
        timestampLocal = datetime.datetime.now()
        html_soup = BeautifulSoup(response.text, 'html.parser')
        localNews = []
        
        for article in html_soup.find_all('article', attrs={"class": re.compile("^ContentTeaser")}):
            entry = {}
            overline = article.find('div', attrs={"class": re.compile("^Overline")})
            headline = article.find('h2', attrs={"class": re.compile("^Headline")})
            link = article.parent.get('href')

            if overline == None or headline == None or link == None:
                continue

            title : str = overline.get_text() + " - " + headline.get_text()
            title = title.replace("Kostenpflichtig", "")
            title = re.sub('[\s]+', ' ', title)
            entry["title"] = title.strip()
            entry["link"] = 'https://www.saechsische.de' + link
            teaser = article.find('p', attrs={"class":  re.compile("^TeaserText")})
            entry["teaser"] = teaser.get_text().strip() if teaser is not None else ""
            localNews.append(entry)

    return localNews

@app.get("/school")
async def getSchoolNews():
    global schoolNews, timestampSchool
    if (not schoolNews or (datetime.datetime.now() - timestampSchool).total_seconds() > cacheExpirationTime):
        print("crawling latest data...")

        url = 'https://www.franziskaneum.de/wordpress/category/aktuelles/'
        response = get(url)
        timestampSchool = datetime.datetime.now()
        html_soup = BeautifulSoup(response.text, 'html.parser')
        schoolNews = []

        for article in html_soup.find_all('article', class_='post'):
            entry = {}
            title =  article.find(class_='entry-title')
            link = article.find(class_='entry-title').find('a')
            teaser = article.find(class_='post-content').find('div', class_='entry-content')
            
            if title == None or link == None: # skip invalid occurences
                continue

            teaser = re.sub('([\t\n\\\/]+|(Weiterlesen))', ' ', teaser.get_text()) #replace unwanted stuff with whitespaces
            teaser = re.sub('[\s]+', ' ', teaser) #remove multiple whitespaces
            entry["title"] = title.get_text().strip() # strip() removes leading and trailing whitespaces
            entry["link"] = link.get('href')
            entry["teaser"] = teaser.strip() if teaser is not None else ""
            schoolNews.append(entry)

    return schoolNews

@app.get("/global")
async def getGlobalNews():
    return "TODO: implement"
