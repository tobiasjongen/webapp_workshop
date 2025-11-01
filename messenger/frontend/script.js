// Create WebSocket connection.
const socket = new WebSocket("ws://192.168.178.24:8765");

let username = '';

function startChat() {
    // Save name
    const nameInput = document.querySelector('#login-page input');
    username = nameInput.value;

    // Hide login page
    const loginPage = document.getElementById('login-page');
    loginPage.style.display = 'none';

    // Show chat page
    const chatPage = document.getElementById('chat-page');
    chatPage.style.display = 'block';
}

function sendMessage() {
    // Read message
    const chatInput = document.querySelector('#chat-page input');
    const message = chatInput.value;

    // Send message to server
    const messageObject = {
        user: username,
        content: message
    };
    const messageString = JSON.stringify(messageObject);
    socket.send(messageString);

    // Delete message from input
    chatInput.value = '';
}

socket.addEventListener('message', function(event) {
    const messageList = JSON.parse(event.data);

    console.log(event.data)

    for (const message of messageList) {
        /**
         * Build an HTML element that looks like this:
         * 
         *  <div class="message">
         *      <span class="author">Konrad</span>
         *      <span class="time">1.11.2025, 14:57:50</span>
         *      <span class="text">Hallo Welt!</span>
         *  </div>
         */
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');

        const authorElement = document.createElement('span');
        authorElement.classList.add('author');
        authorElement.innerText = message.user;
        messageElement.appendChild(authorElement);
        
        const timeElement = document.createElement('span');
        timeElement.classList.add('time');
        timeElement.innerText = new Date(message.timestamp).toLocaleString();
        messageElement.appendChild(timeElement);

        const textElement = document.createElement('span');
        textElement.classList.add('text');
        textElement.innerText = message.content;
        messageElement.appendChild(textElement);
        
        const messageContainer = document.getElementById('message-container');
        messageContainer.appendChild(messageElement);
    }
});
