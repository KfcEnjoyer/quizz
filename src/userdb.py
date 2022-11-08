import psycopg2


def connect():
    connection = psycopg2.connect(database='users',
                                  host='localhost',
                                  user='postgres',
                                  password='lolkek12')
    return connection


def create_users_table():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username varchar(80) UNIQUE, "
            "password varchar(80) NOT NULL)")
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


def get_user(name: str):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"SELECT id from users WHERE username='{name}'")
        conn.commit()
        return cur.fetchone()[0]
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()


def create_results_table():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS results (userid int, quiz_name VARCHAR,"
                    f" score int)")
        conn.commit()
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()


def insert_results(ID: int, quiz_name: str, score: int):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO results (userid, quiz_name,"
                    f" score)"
                    f" VALUES ({ID}, '{quiz_name}', {score})")
        conn.commit()
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()
