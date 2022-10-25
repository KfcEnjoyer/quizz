import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/for_python"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class users(db.Model):
    __tablename__ = 'users'

    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, student_name, password):
        self.student_name = student_name
        self.password = password

    def __repr__(self):
        return f"<Student {self.student_name}>"


#def check_user(uname, pswd):


# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/login', methods=['GET', 'POST'])
# def result():
#     print(requests)
#     print(request.form)
#     student_name = request.form['sname']
#     password = request.form['pswd']
#     usr = users(student_name=[student_name], password=[password])
#     db.session.add(usr)
#     db.session.commit()
#     return f"Hello {student_name}"
#
# if __name__ == '__main__':
#     app.run(debug=True)



