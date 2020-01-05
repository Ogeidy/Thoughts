import datetime
import argparse


from core_thoughts import *





"""Parsing input arguments"""
parser = argparse.ArgumentParser(description="Some description")
parser.add_argument('action', choices=['get', 'add', 'delete'], default='get', help='Todo')
parser.add_argument('type', choices=['thought', 'mention', 'tag', 'mention_tag'], default='thought', help='Todo')
parser.add_argument('payload', nargs='*', help='Style name')
args = parser.parse_args()

print(args)

conn = create_connection('test.sqlite')
init_db(conn) # ???

if args.action == 'get':
    if args.type == 'thought':
        # print('Thought:')
        for th in select_thought(conn):
            print(th)
    if args.type == 'mention':
        # print('Mention:')
        for th in select_mention(conn):
            print(th)
    if args.type == 'tag':
        # print('Tag:')
        for th in select_querry(conn, 'SELECT * FROM Tag'):
            print(th)
    if args.type == 'mention_tag':
        # print('MentionTag:')
        for th in select_querry(conn, 'SELECT * FROM MentionTag'):
            print(th)
if args.action == 'add':
    if args.type == 'thought':
        create_thought(conn, args.payload)
    if args.type == 'mention':
        add_mention(conn, args.payload)
    if args.type == 'tag':
        create_tag(conn, args.payload)
    if args.type == 'mention_tag':
        pass


# print(create_thought(conn, ('Roper', 'Good')))
# print(create_tag(conn, ('Life',)))
# print(add_mention(conn, (2,)))
# print(add_mention(conn, (3, datetime.datetime(1885, 10, 21, 10, 32))))
# print(add_mentiontag(conn, (1, 1)))

conn.commit()
conn.close()
