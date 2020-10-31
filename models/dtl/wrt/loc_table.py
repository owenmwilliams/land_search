from dtl.api.dtl_loc import shp_get
from est.db.cur import con_cur
import pandas as pd
import json
from io import StringIO
import psycopg2
from psycopg2 import sql

def wrt_loc(a):

    y = shp_get()

    buffer = StringIO()
    y.to_csv(buffer, index_label='id', header=False, sep=';')
    buffer.seek(0)

    cur, con = con_cur()
    try:
        cur.execute(
            sql.SQL("""CREATE TABLE {} (
                series_key serial,
                county_name varchar(80) NOT NULL,
                state_name varchar(80) NOT NULL,
                state varchar(20),
                county varchar(20),
                housing_units int,
                sqmi decimal,
                object_id int PRIMARY KEY,
                geom_poly polygon)
            """).format(sql.Identifier(a)))
        cur.copy_from(buffer, a, sep=";")
    except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            con.rollback()
            cur.close()
    con.commit()
    cur.close()
    