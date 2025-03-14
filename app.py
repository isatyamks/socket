from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# A simple route to verify the server is running.
@app.route("/")
def index():
    return "Chat server is running!"

# Handle incoming messages
@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    # Broadcast the message to all connected clients
    send(msg, broadcast=True)

if __name__ == "__main__":
    # Run the app on all available IP addresses on port 5000.
    socketio.run(app, host="0.0.0.0", port=5000)
