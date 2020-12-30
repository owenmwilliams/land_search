import psycopg2
import socket

def con_cur():
    host = socket.gethostname()
    print(host)
    if host == 'pi0':
        db = "v003"
        port = "5432"
    else:
        db = "owenwilliams"
        port = "5436"
    con = psycopg2.connect(database=db, host=host, port=port)
    cur = con.cursor()
    return cur, con
    
    # if socket.gethostname() = 'pi0':
    #     con = psycopg2.connect(database=db, host="localhost", port="5432")
    #     cur = con.cursor()
    #     return cur, con
    # else:
    #     con = psycopg2.connect(database=db, host=)
    