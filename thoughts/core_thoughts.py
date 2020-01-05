import sqlite3

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
    create_table(conn, SQL_CREATE_MENTION_TABLE)
    create_table(conn, SQL_CREATE_TAG_TABLE)
    create_table(conn, SQL_CREATE_MENTIONTAG_TABLE)


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


def select_mention(conn):
    querry = """SELECT Mention.Id, Thought.Name, datetime(Mention.date, 'localtime')
                FROM Mention INNER JOIN Thought ON Thought.Id = Mention.ThoughtId"""
    return select_querry(conn, querry)


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


def add_mention(conn, mention):
    if len(mention) == 1:
        querry = 'INSERT INTO Mention(ThoughtId) VALUES(?)'
    else:
        querry = 'INSERT INTO Mention(ThoughtId, Date) VALUES(?, ?)'
    return insert_querry(conn, querry, mention)


def add_mentiontag(conn, mention_tag):
    querry = 'INSERT INTO MentionTag(MentionId, TagId) VALUES(?, ?)'
    return insert_querry(conn, querry, mention_tag)



if __name__ == '__main__':
    print('Hello')
