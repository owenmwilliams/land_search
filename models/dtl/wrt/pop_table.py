from dtl.api.dtl_census import census_get, st_fips_get
from est.db.cur import con_cur
import pandas as pd
import json
from io import StringIO
import psycopg2
from psycopg2 import sql

def wrt_pop(a, b):

    y = census_get(b).drop([0])

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

def app_pop(a, b):
    
    y = census_get(b).drop([0])
    
    cur, con = con_cur()

    cur.execute(
            sql.SQL("""SELECT count(*) from {}
            """).format(sql.Identifier(a)))
    pos = cur.fetchone()
    y.index = y.index+pos

    buffer = StringIO()
    y.to_csv(buffer, index_label='id', header=False, sep=';')
    buffer.seek(0)

    try:
        cur.copy_from(buffer, a, sep=";")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        con.rollback()
        cur.close()
    con.commit()
    cur.close()

def census_loop(table_name):    
    x = st_fips_get()
    new_header = x.iloc[0]
    x = x[1:]
    x.columns = new_header
    x.drop_duplicates(subset=['state'], inplace=True)
    try:
        y = x.iloc[1]
        wrt_pop(table_name,y['state'])
        print("Building new table for census data: ", table_name)
    finally:
        for i in range(len(x)-1):
            y = x.iloc[i+1]
            print(y)
            app_pop(table_name,y['state'])        
