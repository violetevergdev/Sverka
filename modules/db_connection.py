import sqlite3


def db_connection():
    db_path = 'db/tmp.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    return conn, c