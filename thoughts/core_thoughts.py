import sqlite3

from thoughts.db_init_strings import *
# from db_init_strings import *


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
        return [tuple(descr[0] for descr in cursor.description)] + cursor.fetchall()
    except sqlite3.OperationalError as exc:
        print('OperationalError\n' + str(exc))
    return None


def select(conn, type):
    result = None
    if (type == 'thought'):
        result = select_querry(conn, 'SELECT * FROM thought')
    elif (type == 'mention'):
        result = select_querry(conn, 'SELECT * FROM mention')
    elif (type == 'tag'):
        result = select_querry(conn, 'SELECT * FROM tag')
    elif (type == 'mention_tag'):
        result = select_querry(conn, 'SELECT * FROM mention_tag')
    elif (type == 'all'):
        querry = """SELECT mention.id, thought.name, thought.description,
                datetime(mention.date, 'localtime') AS date,
                (SELECT GROUP_CONCAT(name) 
                FROM tag INNER JOIN mention_tag ON tag.id=mention_tag.tag_id 
                WHERE mention_tag.mention_id=mention.id) AS tags
                FROM mention INNER JOIN thought ON thought.id = mention.thought_id"""
        result = select_querry(conn, querry)
    return result


def insert_querry(conn, sql_string, params):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_string, params)
        return cursor.lastrowid
    except sqlite3.OperationalError as exc:
        print('OperationalError\n' + str(exc))
    return None


def create_thought(conn, thought):
    querry = 'INSERT INTO thought(name, description) VALUES(?,?)'
    return insert_querry(conn, querry, thought)


def create_tag(conn, tag):
    querry = 'INSERT INTO tag(name) VALUES(?)'
    return insert_querry(conn, querry, tag)


def add_mention(conn, mention):
    if len(mention) == 1:
        querry = 'INSERT INTO mention(thought_id) VALUES(?)'
    else:
        querry = 'INSERT INTO mention(thought_id, date) VALUES(?, ?)'
    return insert_querry(conn, querry, mention)


def add_mentiontag(conn, mention_tag):
    querry = 'INSERT INTO mention_tag(mention_id, tag_id) VALUES(?, ?)'
    return insert_querry(conn, querry, mention_tag)


def delete_thought(conn, thought):
    querry = 'DELETE FROM thought WHERE id=?'
    return insert_querry(conn, querry, thought)


def delete_mention(conn, mention):
    querry = 'DELETE FROM mention WHERE id=?'
    return insert_querry(conn, querry, mention)


def delete_tag(conn, tag):
    querry = 'DELETE FROM tag WHERE id=?'
    return insert_querry(conn, querry, tag)


def delete_mentiontag(conn, mention_tag):
    querry = 'DELETE FROM mention_tag WHERE mention_id=? AND tag_id=?'
    return insert_querry(conn, querry, mention_tag)
