import os
import sqlite3
import sys
from settings.config import env, settings as conf

def db_connection():
    if env == 'prod':
        db_path = os.path.join(sys._MEIPASS, conf.db_path)
    else:
        db_path = conf.db_path

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
    except Exception as e:
        print(e)

    return conn, c