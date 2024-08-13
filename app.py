from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # handle signup logic
        pass
    return render_template("signup.html")

@app.route('/home')
def home():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('home.html', username=username, room=room)
    else:
        return redirect(url_for('signup'))

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info(f"{data['username']} has sent message to the room {data['room']}: {data['message']}")
    socketio.emit('receive_message', data, room=data['room'])

@socketio.on('join')
def handle_join_room_event(data):
    app.logger.info(f"{data['username']} has joined the room {data['room']}")
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])

if __name__ == '__main__':
    socketio.run(app)
