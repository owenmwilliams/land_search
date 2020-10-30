from dtl.api.dtl_census import census_get
import pandas as pd
import json
from est.db.cur import con_cur
from io import StringIO
import psycopg2
from psycopg2 import sql

def wrt_pop(a):

    y = census_get().drop([0])

    buffer = StringIO()
    y.to_csv(buffer, index_label='id', header=False, sep=';')
    buffer.seek(0)

    cur, con = con_cur()
    try:
        cur.execute(
            sql.SQL("""CREATE TABLE {} (
                pkey serial PRIMARY KEY,
                name varchar(80) UNIQUE NOT NULL,
                pop varchar(20),
                state varchar(20),
                county varchar(20))
            """).format(sql.Identifier(a)))
        cur.copy_from(buffer, a, sep=";")
    except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            con.rollback()
            cur.close()
    con.commit()
    cur.close()