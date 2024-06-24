import os
import sqlite3
import sys


def db_connection():
    db_path = os.path.join(sys._MEIPASS, 'db/tmp.db')
    # db_path = 'db/tmp.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    return conn, c