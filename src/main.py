from flask import Flask, render_template, request, redirect, flash, session, url_for
import testdb
from os import urandom
import requests
import random as r

app = Flask(__name__)
app.secret_key = urandom(20)
testdb.create_table()


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/", methods=["POST"])
def login():
    username = request.form['sname']
    passwd = request.form['pswd']
    if testdb.check_user(username, passwd):
        session['sname'] = username
        return redirect("/quiz_setup")
    else:
        flash('Login is invalid!')


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        new_username = request.form['sname']
        psw1 = request.form['psw']
        psw2 = request.form['psw-repeat']
        if len(new_username) < 3:
            flash('Username must be at least 3 characters')
            return redirect(url_for('register'))
        if len(psw1) < 6:
            flash('Password must be at least 6 characters')
            return redirect(url_for('register'))
        if psw1 != psw2:
            flash('Passwords are not matching!')
            return redirect(url_for('register'))
        testdb.add_user(new_username, psw1)
        return redirect("/quiz_setup")
    return render_template("register.html")


@app.route('/log-out')
def log_out():
    session.pop('sname', None)
    return redirect(url_for('home'))


rand1 = r.randint(0, 3)
rand2 = r.randint(0, 3)
while rand2 == rand1:
    rand2 = r.randint(0, 3)
rand3 = r.randint(0, 3)
while rand3 == rand1 or rand3 == rand2:
    rand3 = r.randint(0, 3)
rand4 = r.randint(0, 4)
while rand4 == rand1 or rand4 == rand2 or rand4 == rand3:
    rand4 = r.randint(0, 3)


def check_for_correct_answer(answer, correct_answer) -> bool:
    if answer == correct_answer:
        return True
    return False


# @app.route("/quiz_setup", methods=["POST", "GET"])
# def quiz_setup():
#
#     if request.method == "POST":
#         return redirect("/quiz")
#     return render_template('quiz_setup.html')

# @app.route("/quiz_get", methods=["POST", "GET"])
# def quiz_get(num_of_questions, category, difficulty, type):
#     return requests.get(url=f'https://opentdb.com/api.php?amount={num_of_questions}&category={category}&difficulty={difficulty}&type={type}').json()


@app.route("/quiz_setup", methods=["POST", "GET"])
def quiz():
    num_of_questions = request.form.get('num-of-questions')
    category = request.form.get('category')
    difficulty = request.form.get('difficulty')
    type = request.form.get('type')
    questions = requests.get(url=f'https://opentdb.com/api.php?amount={num_of_questions}&category={category}&difficulty={difficulty}&type={type}').json()
    if request.method == "POST":
        score = 0
        questions_list = []
        for question in questions['results']:
            questions_list.append(question['correct_answer'])
            questions_list.append(question['incorrect_answers'][0])
            questions_list.append(question['incorrect_answers'][1])
            questions_list.append(question['incorrect_answers'][2])
            return render_template('quiz.html', question=question['question'], answer1=questions_list[rand1],
                                   answer2=questions_list[rand2],
                                   answer3=questions_list[rand3],
                                   answer4=questions_list[rand4],
                                   score=score)
    return render_template('quiz_setup.html')


if __name__ == "__main__":
    app.run(debug=True)