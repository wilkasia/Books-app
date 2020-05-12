import mysql.connector

from flask import g


def get_db():
    print("get_db")
    if 'db' not in g:
        g.db = mysql.connector.connect(
            user='booksapp',
            password='az14Gcjs',
            host='localhost',
            port=13306,
            database='booksapp'
        )

    return g.db


def close_db(e=None):
    print("close_db")
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)

