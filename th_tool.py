import datetime
import argparse


from thoughts.core_thoughts import *


"""Parsing input arguments"""
parser = argparse.ArgumentParser(description="Some description")
parser.add_argument('action', choices=['get', 'add', 'delete'], default='get', help='Todo')
parser.add_argument('type', choices=['thought', 'mention', 'tag', 'mention_tag', 'all'], default='thought', help='Todo')
parser.add_argument('payload', nargs='*', help='Style name')
args = parser.parse_args()

conn = create_connection('test.sqlite')
init_db(conn) # ???

if args.action == 'get':
    for th in select(conn, args.type):
        print(th)
if args.action == 'add':
    if args.type == 'thought':
        create_thought(conn, args.payload)
    if args.type == 'mention':
        add_mention(conn, args.payload)
    if args.type == 'tag':
        create_tag(conn, args.payload)
    if args.type == 'mention_tag':
        add_mentiontag(conn, args.payload)
if args.action == 'delete':
    if args.type == 'thought':
        delete_thought(conn, args.payload)
    if args.type == 'mention':
        delete_mention(conn, args.payload)
    if args.type == 'tag':
        delete_tag(conn, args.payload)
    if args.type == 'mention_tag':
        delete_mentiontag(conn, args.payload)

conn.commit()
conn.close()
