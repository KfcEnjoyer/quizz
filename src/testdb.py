import psycopg2


def connect():
    connection = psycopg2.connect(database='pyp',
                                  host='localhost',
                                  user='postgres',
                                  password='lolkek12')
    return connection


def create_table():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username varchar(80), "
            "password varchar(80) NOT NULL)")
        conn.commit()
    except EOFError as err:
        print("Error has occured", err)
    finally:
        cur.close()
        conn.close()


def add_user(username, password):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        conn.commit()
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()


def check_user(username, password):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"SELECT EXISTS(SELECT * FROM users WHERE username='{username}' AND password='{password}')")
        conn.commit()
        return cur.fetchone()[0]
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()
