import eventlet
eventlet.monkey_patch()  # Must be called before any other imports!

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize SocketIO with eventlet support.
socketio = SocketIO(app)

# Set up logging with rotation: rotate every hour, keep backups for 24 hours.
logger = logging.getLogger('chat_app')
logger.setLevel(logging.INFO)
log_handler = TimedRotatingFileHandler('chat.log', when='H', interval=1, backupCount=24)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

@app.route('/')
def index():
    # Render a basic chat interface.
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    # Log and print the incoming message.
    logger.info("Message received: %s", msg)
    print("Received message: " + msg)
    # Broadcast the message to all connected clients.
    send(msg, broadcast=True)

if __name__ == '__main__':
    # Use the PORT environment variable (set by Render) or default to 5000.
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
