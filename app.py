from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def signup():
    return render_template("signup.html")

@app.route('/home')
def home():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('home.html', username=username, room=room)
    else:
        return redirect(url_for('signup'))

@socketio.on('join')
def handle_join_room_event(data):
    app.logger.info(f"{data['username']} has joined the room {data['room']}")

if __name__ == '__main__':
    socketio.run(app, debug=True)
