from dtl.api.dtl_census import census_get
from est.db.cur import con_cur
import pandas as pd
import json
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
                updated date,
                date_code int,
                name varchar(80),
                pop varchar(20),
                race int,
                sex int,
                age_group int,
                hisp int,
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
    