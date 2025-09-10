document.addEventListener('DOMContentLoaded', function() {
    displayNews();
}, false);

async function getNews(path) {
    try {
        const resp = await fetch("http://localhost:8000/" + path);
        if (!resp.ok) {
            throw new Error(`HTTP error! status: ${resp.status}`);
        }
        return await resp.json();
    } catch (error) {
        console.error('Error fetching news:', error);
        return [];
    }
}

function createNewsEntry(news) {
    let div = document.createElement("div");
    div.classList.add("newsEntry");

    let title = document.createElement("h3");
    title.textContent = news.title;

    let teaser = document.createElement("p");
    teaser.textContent = news.teaser;

    div.onclick = function(){
        if (news.link) {
            window.open(news.link, '_blank').focus();
        }
    };

    div.appendChild(title);
    div.appendChild(teaser);

    return div;
}

async function displayNews() {
    const schoolNewsNode = document.getElementById("schoolNews");
    const localNewsNode = document.getElementById("localNews");

    // Load school news
    try {
        const schoolNews = await getNews("school");
        console.log('School news:', schoolNews);
        
        if (!schoolNews || schoolNews.length === 0) {
            const noNews = document.createElement("p");
            noNews.textContent = "Im Moment sind keine Neuigkeiten aus der Schule verfügbar.";
            noNews.classList.add("no-news");
            schoolNewsNode.appendChild(noNews);
        } else {
            schoolNews.forEach(element => {
                schoolNewsNode.appendChild(createNewsEntry(element));
            });
        }
    } catch (error) {
        console.error('Error loading school news:', error);
    }

    // Load local news
    try {
        const localNews = await getNews("local");
        console.log('Local news:', localNews);
        
        if (!localNews || localNews.length === 0) {
            const noNews = document.createElement("p");
            noNews.textContent = "Im Moment sind keine lokalen Neuigkeiten verfügbar.";
            noNews.classList.add("no-news");
            localNewsNode.appendChild(noNews);
        } else {
            localNews.forEach(element => {
                localNewsNode.appendChild(createNewsEntry(element));
            });
        }
    } catch (error) {
        console.error('Error loading local news:', error);
    }
}