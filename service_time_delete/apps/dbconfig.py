from apps.server import app
from functools import wraps
import sqlite3

global configdb

configdb = {"db_name" : "../project/store-file.db" }

def connect_sqlite():
    def wrap(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Setup connection
                connection = sqlite3.connect(configdb["db_name"])
                cursor = connection.cursor()
                cursor.row_factory = sqlite3.Row
                return_val = fn(cursor, *args, **kwargs)
            except Exception as e : 
                return "connect_sqlite ERROR :" + str(e)
            finally:
                # Close connection
                connection.commit()
                connection.close()
            return return_val
        return wrapper
    return wrap

def create_table_accounts():
    try:
        # Setup connection
        connection = sqlite3.connect(configdb["db_name"])
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
        (uuid text,
        username TEXT NOT NULL UNIQUE,
        password text)''')
        connection.commit()
        connection.close()
    except Exception as e : 
        return "create_table_accounts ERROR : "+str(e)

create_table_accounts()