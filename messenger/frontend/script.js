const API_BASE_URL = 'http://localhost:8000';
let currentUsername = '';
let messageInterval;

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

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        currentUsername = username;
        document.getElementById('currentUsername').textContent = username;
        
        // Switch to chat view
        document.getElementById('loginSection').style.display = 'none';
        document.getElementById('chatSection').style.display = 'block';
        document.getElementById('userInfo').style.display = 'block';
        
        // Load messages and start polling
        await loadMessages();
        startMessagePolling();
        
        errorDiv.textContent = '';
    } catch (error) {
        errorDiv.textContent = error.message;
    }
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const content = messageInput.value.trim();
    
    if (!content) return;

    try {
        const response = await fetch(`${API_BASE_URL}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: currentUsername,
                content: content
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to send message');
        }

        messageInput.value = '';
        messageInput.style.height = 'auto';
        await loadMessages();
    } catch (error) {
        alert('Failed to send message: ' + error.message);
    }
}

async function loadMessages() {
    try {
        const response = await fetch(`${API_BASE_URL}/messages`);
        
        if (!response.ok) {
            throw new Error('Failed to load messages');
        }

        const messages = await response.json();
        displayMessages(messages);
    } catch (error) {
        console.error('Error loading messages:', error);
        document.getElementById('messagesContainer').innerHTML = 
            '<div class="error">Failed to load messages. Please refresh the page.</div>';
    }
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

function startMessagePolling() {
    // Poll for new messages every 2 seconds
    messageInterval = setInterval(loadMessages, 2000);
}

function stopMessagePolling() {
    if (messageInterval) {
        clearInterval(messageInterval);
        messageInterval = null;
    }
}

function logout() {
    currentUsername = '';
    stopMessagePolling();
    
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

// Check if backend is available on page load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (!response.ok) {
            throw new Error('Backend not accessible');
        }
    } catch (error) {
        document.getElementById('loginError').textContent = 
            'Cannot connect to server. Please make sure the backend is running on http://localhost:8000';
    }
});
