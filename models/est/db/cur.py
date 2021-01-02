import psycopg2
import socket
import os
from dotenv import load_dotenv

def con_cur():
    host = socket.gethostname()
    load_dotenv()
    version = os.getenv("version").replace('.','')

    if host == 'pi0':
        db = version
        port = "5432"
    else:
        db = "owenwilliams"
        port = "5436"
    con = psycopg2.connect(database=db, host=host, port=port)
    cur = con.cursor()
    return cur, con
    