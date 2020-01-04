import sqlite3
import datetime

from db_init_strings import *


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as exc:
        print(exc)
    return conn


def create_table(conn, sql_string):
    try:
        conn.cursor().execute(sql_string)
    except Exception as exc:
        print(exc)


def init_db(conn):
    create_table(conn, SQL_CREATE_THOUGHT_TABLE)
    create_table(conn, SQL_CREATE_THOUGHTS_TABLE)
    create_table(conn, SQL_CREATE_TAG_TABLE)
    create_table(conn, SQL_CREATE_THOUGHTTAG_TABLE)


def select_querry(conn, sql_string):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_string)
        return cursor.fetchall()
    except sqlite3.OperationalError as exc:
        print('OperationalError\n' + str(exc))
    return None


def select_thought(conn):
    return select_querry(conn, 'SELECT * FROM Thought')


def select_thoughts(conn):
    return select_querry(conn, 'SELECT * FROM Thoughts')


def insert_querry(conn, sql_string, params):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_string, params)
        return cursor.lastrowid
    except sqlite3.OperationalError as exc:
        print('OperationalError\n' + str(exc))
    return None


def create_thought(conn, thought):
    querry = 'INSERT INTO Thought(Name, Description) VALUES(?,?)'
    return insert_querry(conn, querry, thought)


def create_tag(conn, tag):
    querry = 'INSERT INTO Tag(Name) VALUES(?)'
    return insert_querry(conn, querry, tag)


def add_thoughts(conn, thoughts):
    querry = 'INSERT INTO Thoughts(ThoughtId, Date) VALUES(?, ?)'
    return insert_querry(conn, querry, thoughts)


def add_thoughttag(conn, thought_tag):
    querry = 'INSERT INTO ThoughtTag(ThoughtId, TagId) VALUES(?, ?)'
    return insert_querry(conn, querry, thought_tag)



if __name__ == '__main__':
    conn = create_connection('test.sqlite')
    init_db(conn)

    # print(create_thought(conn, ('Hello', 'WTF???')))
    # print(create_tag(conn, ('Life',)))
    # print(add_thoughts(conn, (3, '10.10.2015')))
    # print(add_thoughttag(conn, (2, 2)))

    print('Thought:')
    for th in select_thought(conn):
        print(th)
    print('Thoughts:')
    for th in select_thoughts(conn):
        print(th)
    print('Tag:')
    for th in select_querry(conn, 'SELECT * FROM Tag'):
        print(th)
    print('ThoughtTag:')
    for th in select_querry(conn, 'SELECT * FROM ThoughtTag'):
        print(th)

    print(datetime.date(2019, 12, 27))
    print(datetime.date.today())

    conn.commit()
    conn.close()
