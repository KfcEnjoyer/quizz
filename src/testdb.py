import psycopg2


def connect():
    connection = psycopg2.connect(database='postgres',
                                  host='localhost',
                                  user='postgres',
                                  password='lolkek12')
    return connection


def check_if_table_exists(quiz_name: str):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT EXISTS("
                    " SELECT FROM"
                    " pg_tables"
                    " WHERE"
                    " schemaname = 'public' AND"
                    f" tablename = '{quiz_name}')")
        conn.commit()
        return cur.fetchone()[0]
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()


def create_quiz_table(name: str):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {name} (table_name VARCHAR, id SERIAL PRIMARY KEY, question VARCHAR(300),"
                    f" correct_answer VARCHAR(200),"
                    f" incorrect_answer1 VARCHAR(200),"
                    f" incorrect_answer2 VARCHAR(200),"
                    f" incorrect_answer3 VARCHAR(200))")
        conn.commit()
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()


def insert_questions(name: str, question: str, correct_answer: str, incorrect_answer1: str, incorrect_answer2: str, incorrect_answer3: str):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {name} (table_name,"
                    f" question,"
                    f" correct_answer, "
                    f" incorrect_answer1,"
                    f" incorrect_answer2,"
                    f" incorrect_answer3)"
                    f"VALUES ('{name}', '{question}', '{correct_answer}', '{incorrect_answer1}', '{incorrect_answer2}', '{incorrect_answer3}')")
        conn.commit()
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()


def get_questions(name: str):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"SELECT question, correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3 FROM {name}")
        return cur.fetchall()
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()


def get_num_of_questions(name: str):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"SELECT count(*) FROM {name}")
        return cur.fetchone()[0]
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()


def get_quiz_name(name: str):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f"SELECT table_name FROM {name}")
        return cur.fetchall()
    except EOFError as err:
        print("Error has occurred", err)
    finally:
        cur.close()
        conn.close()
