import eventlet
eventlet.monkey_patch() 

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request
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

users = {}

@app.route('/')
def index():
    return "Chat server is running"

@socketio.on('join')
def on_join(username):
    if username in users.values():
        emit('error', {'msg': 'Username already taken. Please choose a different one.'})
        return
    users[request.sid] = username
    msg = f"{username} has joined the chat."
    send(msg, broadcast=True)
    logger.info(msg)

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Anonymous")
    full_msg = f"{username}: {msg}"
    send(full_msg, broadcast=True)
    logger.info(full_msg)

@socketio.on('disconnect')
def on_disconnect():
    username = users.pop(request.sid, None)
    if username:
        msg = f"{username} has left the chat."
        send(msg, broadcast=True)
        logger.info(msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
