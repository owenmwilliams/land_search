import psycopg2
import socket

def con_cur():
    host = socket.gethostname()

    if host == 'pi0':
        db = 'v016'
        port = "5432"
    else:
        db = "owenwilliams"
        port = "5436"
    con = psycopg2.connect(database=db, host=host, port=port, user='postgres')
    cur = con.cursor()
    return cur, con
    