const WS_URL = 'ws://localhost:8000/ws';
let currentUsername = '';
let messageInterval;
let ws = null;

// Handle Enter key in login input
document.getElementById('usernameInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        login();
    }
});

// Handle Enter key in message input (Shift+Enter for new line)
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-resize message input
document.getElementById('messageInput').addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 100) + 'px';
});

async function login() {
    const username = document.getElementById('usernameInput').value.trim();
    const errorDiv = document.getElementById('loginError');
    
    if (!username) {
        errorDiv.textContent = 'Please enter your name';
        return;
    }

    currentUsername = username;
    document.getElementById('currentUsername').textContent = username;

    // Switch to chat view
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('chatSection').style.display = 'block';
    document.getElementById('userInfo').style.display = 'block';

    connectWebSocket();
    errorDiv.textContent = '';
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const content = messageInput.value.trim();
    
    if (!content) return;

    try {
        // Prefer WebSocket when available
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'send_message', username: currentUsername, content }));
            // clear input immediately; server will broadcast the message back to us
            messageInput.value = '';
            messageInput.style.height = 'auto';
            return;
        }
        alert('WebSocket not connected. Message not sent.');
    } catch (error) {
        alert('Failed to send message: ' + error.message);
    }
}


function connectWebSocket() {
    if (ws) return; // already connected or connecting

    ws = new WebSocket(WS_URL);

    ws.addEventListener('open', () => {
        console.log('WebSocket connected');
    });

    ws.addEventListener('message', (ev) => {
        try {
            const data = JSON.parse(ev.data);
            if (data.type === 'init_sync') {
                displayMessages(data.messages || []);
            } else if (data.type === 'new_message') {
                appendMessage(data.message);
            }
        } catch (e) {
            console.error('Invalid WS message', e);
        }
    });

    ws.addEventListener('close', () => {
        console.log('WebSocket closed');
        ws = null;
        // Optionally attempt reconnect after a delay
        setTimeout(() => {
            if (!ws && currentUsername) connectWebSocket();
        }, 2000);
    });

    ws.addEventListener('error', (err) => {
        console.error('WebSocket error', err);
    });
}


function appendMessage(message) {
    const container = document.getElementById('messagesContainer');

    const placeholder = container && (container.querySelector('.no-messages') || container.querySelector('.loading'));
    if (placeholder) container.innerHTML = '';

    const isOwn = message.username === currentUsername;
    const div = document.createElement('div');
    div.className = `message ${isOwn ? 'own' : ''}`;
    div.innerHTML = `
        <div class="message-header">
            <span class="username">${escapeHtml(message.username)}</span>
            <span class="timestamp">${message.timestamp}</span>
        </div>
        <div class="message-content">${escapeHtml(message.content)}</div>
    `;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function displayMessages(messages) {
    const container = document.getElementById('messagesContainer');
    
    if (messages.length === 0) {
        container.innerHTML = '<div class="no-messages">No messages yet. Start the conversation!</div>';
        return;
    }

    const messagesHTML = messages.map(message => {
        const isOwn = message.username === currentUsername;
        return `
            <div class="message ${isOwn ? 'own' : ''}">
                <div class="message-header">
                    <span class="username">${escapeHtml(message.username)}</span>
                    <span class="timestamp">${message.timestamp}</span>
                </div>
                <div class="message-content">${escapeHtml(message.content)}</div>
            </div>
        `;
    }).join('');

    container.innerHTML = messagesHTML;
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

function logout() {
    currentUsername = '';
    // Close websocket if open
    if (ws) {
        try { ws.close(); } catch (e) {}
        ws = null;
    }
    
    // Switch back to login view
    document.getElementById('chatSection').style.display = 'none';
    document.getElementById('loginSection').style.display = 'block';
    document.getElementById('userInfo').style.display = 'none';
    
    // Clear inputs
    document.getElementById('usernameInput').value = '';
    document.getElementById('messageInput').value = '';
    document.getElementById('loginError').textContent = '';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
