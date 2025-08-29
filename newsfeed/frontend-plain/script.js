document.addEventListener('DOMContentLoaded', function() {
    displayNews();
  }, false);

async function getNews(path) {
    const resp = await fetch("http://localhost:8000/" + path);
    return await resp.json()
}

function createNewsEntry(news) {
    let div = document.createElement("div");
    div.classList.add("newsEntry");

    let title = document.createElement("span");
    title.id = "title";
    title.textContent = news.title;

    div.onclick = function(){window.open(news.link, '_blank').focus();};

    let teaser = document.createElement("span");
    teaser.id = "teaser";
    teaser.textContent = news.teaser;

    div.appendChild(title);
    div.appendChild(teaser);

    return div;
}

async function displayNews() {
    let schoolNews = await getNews("school");
    console.log(schoolNews);

    let schoolNewsNode = document.getElementById("schoolNews");
    schoolNews.forEach(element => {
        schoolNewsNode.appendChild(createNewsEntry(element));
    });
}