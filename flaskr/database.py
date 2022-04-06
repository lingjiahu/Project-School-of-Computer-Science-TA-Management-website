import sqlite3
from flask import g
from flaskr import app

def connect_db():
    # Connect to the database
    return sqlite3.connect(app.config['DATABASE'])
    
def get_db():
    # Open a database connection if and only if there is none yet, for the current application context
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def query_db(query,args=(),one=False):
        cur = get_db().execute(query,args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv