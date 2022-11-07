from flask import Flask, render_template, request, redirect, flash, session, url_for
import testdb
from os import urandom
import requests
import random as r

app = Flask(__name__)
app.secret_key = urandom(20)
testdb.create_users_table()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        passwd = request.form['password']
        if testdb.check_user(username, passwd):
            session['username'] = username
            return redirect("/quiz_setup")
        else:
            flash('Login is invalid!')
            return redirect('/register')
    return render_template('login.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        new_username = request.form['new-usname']
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
            return redirect(url_for('register.html'))
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


@app.route("/quiz_setup", methods=["POST", "GET"])
def quiz_setup():
    if request.method == "POST":
        name = request.form['quiz_name']
        num_of_questions = request.form['number']
        category = request.form['category']
        difficulty = request.form['difficulty']
        quiz_type = request.form['type']
        questions = requests.get(
            url=f'https://opentdb.com/api.php?amount={num_of_questions}&category={category}&difficulty={difficulty}&type={quiz_type}').json()
        testdb.create_quiz_table(name)
        for question in questions['results']:
            testdb.insert_questions(name, question['question'], question['correct_answer'],
                                    question['incorrect_answers'][0], question['incorrect_answers'][1],
                                    question['incorrect_answers'][2])
        return redirect('/quiz')
    return render_template('quiz_setup.html')


global score, index
score = 0
index = 0


@app.route("/quiz", methods=["POST", "GET"])
def quiz():
    questions = testdb.get_questions('quizz')
    questions_num = testdb.get_num_of_questions('quizz')
    global index, score
    if request.method == "POST":
        answer = request.form['option']
        if check_for_correct_answer(answer, questions[index][1]):
            score += 1
        index += 1
        if index == questions_num:
            index = 0
            score = 0
        return render_template('questions.html', score=score, question_num=index+1, question=questions[index][0],
                               num_of_quest=questions_num, answer1=questions[index][1], answer2=questions[index][2],
                               answer3=questions[index][3], answer4=questions[index][4])
    index = 0
    return render_template('questions.html', score=score, question_num=index+1, question=questions[index][0],
                           num_of_quest=questions_num, answer1=questions[index][1], answer2=questions[index][2],
                           answer3=questions[index][3], answer4=questions[index][4])


def check_for_correct_answer(answer, correct_answer) -> bool:
    return answer == correct_answer


# 'test.html', number_of_questions=questions_num, question=questions[i][0], answer1=questions[i][1], answer2=questions[i][2], answer3=questions[i][3], answer4=questions[i][4]


if __name__ == "__main__":
    app.run(debug=True)
