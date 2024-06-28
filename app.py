from flask import Flask, render_template, request, redirect, url_for
from flask_sock
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
