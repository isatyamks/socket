let socket;
let username;
let room = "MainRoom";

function login() {
    username = document.getElementById('username').value.trim();
    if (!username) {
        alert("Please enter a username!");
        return;
    }

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('chat-screen').style.display = 'block';
            initializeSocket();
        }
    });
}

function initializeSocket() {
    socket = io();

    socket.emit('join', { username, room });

    socket.on('message', data => {
        const messagesDiv = document.getElementById('messages');
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.username}: ${data.message}`;
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}

function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('message', { username, room, message });
        messageInput.value = '';
    }
}
