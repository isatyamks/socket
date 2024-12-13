from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active users and rooms
users = {}
rooms = {}

@app.route('/')
def home():
    return "Real-Time Chat API is Running!"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user_id = str(uuid.uuid4())
    users[user_id] = username
    return jsonify({"user_id": user_id, "username": username}), 200

@app.route('/rooms', methods=['GET', 'POST'])
def manage_rooms():
    if request.method == 'GET':
        return jsonify({"rooms": list(rooms.keys())}), 200

    if request.method == 'POST':
        data = request.json
        room_name = data.get('room_name')
        if not room_name:
            return jsonify({"error": "Room name is required"}), 400

        if room_name in rooms:
            return jsonify({"error": "Room already exists"}), 400

        rooms[room_name] = []
        return jsonify({"message": f"Room '{room_name}' created successfully!"}), 201

@socketio.on('join')
def handle_join(data):
    username = data.get('username')
    room = data.get('room')
    if not username or not room:
        return send({"error": "Username and room are required"})

    join_room(room)
    rooms[room].append(username)
    send({"message": f"{username} has joined the room."}, to=room)

@socketio.on('leave')
def handle_leave(data):
    username = data.get('username')
    room = data.get('room')
    if not username or not room:
        return send({"error": "Username and room are required"})

    leave_room(room)
    if username in rooms[room]:
        rooms[room].remove(username)
    send({"message": f"{username} has left the room."}, to=room)

@socketio.on('message')
def handle_message(data):
    username = data.get('username')
    room = data.get('room')
    message = data.get('message')
    if not username or not room or not message:
        return send({"error": "Username, room, and message are required"})

    send({"username": username, "message": message}, to=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
