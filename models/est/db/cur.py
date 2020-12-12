import psycopg2

def con_cur():
    con = psycopg2.connect(database='owenwilliams', host="localhost", port="5432")
    cur = con.cursor()
    return cur, con
    