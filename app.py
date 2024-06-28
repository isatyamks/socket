from flask import Flask,render_template,request,redirect





app = Flask(__name__)

@app.route('/')
def signup():
    return render_template("signup.html")

@app.route('/home')
def home():
    username = request.args.get('username')
    room = request.args.get('room')


    if username and room:
        return render_template('home.html')
    else:
        return redirect

if __name__ == '__main__':
    app.run(debug=True)