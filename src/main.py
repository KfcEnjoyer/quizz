from flask import Flask, render_template, request, redirect, flash
import testdb
import requests
import random as r

app = Flask(__name__)
app.secret_key = '12345'

testdb.create_table()

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/", methods=["POST"])
def login():
    username = request.form['sname']
    passwd = request.form['pswd']
    if testdb.check_user(username, passwd):
        return redirect("/quiz")
    else:
        return redirect("/register")


@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        new_username = request.form['new-usname']
        psw1 = request.form['psw']
        psw2 = request.form['psw-repeat']
        if len(new_username) < 3:
            flash('Username must be at least 3 characters', category='error')
            return redirect("/register")
        if len(psw1) < 6:
            flash('Password must be at least  characters', category='error')
            return redirect("/register")
        if psw1 != psw2:
            flash('Passwords are not matching!', category='error')
            return redirect("/register")
        testdb.add_user(new_username, psw1)
        return redirect("/quiz")
    return render_template("register.html")


@app.route("/quiz")
def quiz_page():
    return render_template('quiz.html')



def correct_answer(ans: str, correct_ans) -> bool:
    if ans == correct_ans:
        return True
    return False


rand1 = r.randint(0, 2)
rand2 = r.randint(0, 2)
while rand2 == rand1:
    rand2 = r.randint(0, 2)
rand3 = r.randint(0, 2)
while rand3 == rand1 or rand3 == rand2:
    rand3 = r.randint(0, 2)

score = 0
question = requests.get(url='https://opentdb.com/api.php?amount=10&category=17&difficulty=easy&type=multiple').json()
for quest in question['results']:
    print(quest['question'])
    print(quest['correct_answer'])
    print(quest['incorrect_answers'][rand1])
    print(quest['incorrect_answers'][rand2])
    print(quest['incorrect_answers'][rand3])
    answer = input()
    if correct_answer(answer, quest['correct_answer']):
        score += 1
        print("You are correct!")
        print("Your score is ", score)
    else:
        print("You are incorrect!")
if __name__ == "__main__":
    app.run(debug=True)
