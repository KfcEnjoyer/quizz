import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2
from psycopg2 import Error

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/for_python"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def result():
    print(requests)
    print(request.form)
    student_name = request.form['username']
    password = request.form['password']
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="for_python")
    cursor = connection.cursor()

    def checking(n, d):
        cursor.execute(f"select exists(select * from users where student_name='{n}' and password='{d}')")
        return cursor.fetchone()[0]

    if checking(student_name, password):
        return f"Welcome, {student_name}"
    else:
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="postgres",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="for_python")
            cursor = connection.cursor()
            insert_query = """ INSERT INTO users (student_name, password) VALUES (%s, %s)"""
            item_tuple = (student_name, password)
            cursor.execute(insert_query, item_tuple)
            connection.commit()
            print("Data was successfully inserted")


        except (Exception, Error) as error:
            print("Error", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Connection to PostgreSQL is closed")
        return "You were successfully registered!"



if __name__ == '__main__':
    app.run(debug=True)



