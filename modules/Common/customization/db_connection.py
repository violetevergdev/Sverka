import os, sqlite3, sys
from settings.settings import env

def db_connection():
    if env == "prod":
        db_path = os.path.join(sys._MEIPASS, "db/tmp.db")
    else:
        db_path = "./db/tmp.db"
        
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
    except Exception as e:
        try:
            print(e)
        finally:
            e = None
            del e
    else:
        return conn, c
