var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.6.3.min.js'; // Check https://jquery.com/ for the current version
document.getElementsByTagName('head')[0].appendChild(script);

console.log("Hello World!")

function getRandomQuestion() {
    $.get("http://localhost:8000/", (data, status) => {
        console.log(data);
      })
}