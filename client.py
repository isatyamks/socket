import eventlet
eventlet.monkey_patch()  # Must be called before any other imports!

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Configure rotating logging (rotate every hour; keep last 24 hours)
logger = logging.getLogger('chat_app')
logger.setLevel(logging.INFO)
log_handler = TimedRotatingFileHandler('chat.log', when='H', interval=1, backupCount=24)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

# Dictionary to keep track of connected users: { session_id: username }
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(username):
    # Check if the username is already taken by any connected user.
    if username in users.values():
        # Emit an error back to the client.
        emit('error', {'msg': 'Username already taken. Please choose a different one.'})
        return
    # Save the username associated with this client's session id.
    users[request.sid] = username
    msg = f"{username} has joined the chat."
    send(msg, broadcast=True)
    logger.info(msg)

@socketio.on('message')
def handle_message(msg):
    # Retrieve the username for the client that sent the message.
    username = users.get(request.sid, "Anonymous")
    full_msg = f"{username}: {msg}"
    send(full_msg, broadcast=True)
    logger.info(full_msg)

@socketio.on('disconnect')
def on_disconnect():
    username = users.pop(request.sid, "Anonymous")
    msg = f"{username} has left the chat."
    send(msg, broadcast=True)
    logger.info(msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
