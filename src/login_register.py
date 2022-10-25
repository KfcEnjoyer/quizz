from flask import Flask, render_template, request, redirect, flash
import userdb

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=["POST"])
def login():
    username = request.form['sname']
    passwd = request.form['pswd']
    if userdb.check_user(username, passwd):
        return redirect("/quizz")
    else:
        redirect('/register')


@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        new_username = request.form['new-usname']
        psw1 = request.form['psw']
        psw2 = request.form['psw-repeat']
        if len(new_username) < 3:
            flash('Username must be at least 3 characters', category='error')
        elif len(psw1) < 6:
            flash('Password must be at least  characters', category='error')
        elif psw1 != psw2:
            flash('Passwords are not matching!', category='error')
        else:

            return redirect('/quizz')
    return render_template('register.html')


@app.route("/quizz")
def quiz_page():
    return render_template('quizz.html')
