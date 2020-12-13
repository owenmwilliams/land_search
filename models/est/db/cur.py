import psycopg2

db = "v002"

def con_cur():
    con = psycopg2.connect(database=db, host="localhost", port="5432")
    cur = con.cursor()
    return cur, con
    