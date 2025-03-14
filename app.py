import eventlet
eventlet.monkey_patch()  # Must be the first thing executed

from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route("/")
def index():
    return "Chat server is running!"

@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    send(msg, broadcast=True)

if __name__ == "__main__":
    # Use the PORT environment variable for Render deployments
    import os
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
