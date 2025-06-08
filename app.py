import eventlet
eventlet.monkey_patch() 

import os
import logging
import time
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
last_message_time = 0
message_delay = 0.1  # 100ms delay between messages

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
    global last_message_time
    username = users.get(request.sid, "Anonymous")
    full_msg = f"{username}: {msg}"
    
    # Add a small delay if messages are coming too quickly
    current_time = time.time()
    if current_time - last_message_time < message_delay:
        eventlet.sleep(message_delay)
    
    send(full_msg, broadcast=True)
    logger.info(full_msg)
    last_message_time = time.time()

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
