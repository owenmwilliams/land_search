from dtl.api.dtl_census import census_get, st_fips_get
from est.db.cur import con_cur
import pandas as pd
import numpy as np
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

# TODO: this loop is clunky af

def census_loop(table_name):    
    x = st_fips_get()
    new_header = x.iloc[0]
    x = x[1:]
    x.columns = new_header
    x.drop_duplicates(subset=['state'], inplace=True)
    dup_x = x
    try:
        cur, con = con_cur()
        sql = "SELECT DISTINCT state from %s;" % table_name
        dat = pd.read_sql_query(sql, con)
        dat = np.squeeze(dat.values.tolist())
        cur.close()
        for i in range(len(dup_x)):
            z = dup_x.iloc[i]
            if z['state'] in dat:
                x = x[x.state != z['state']]
        trig = 1      
    except pd.io.sql.DatabaseError:
        print("Building new table for census data: ", table_name)
        y = x.iloc[0]
        wrt_pop(table_name,y['state'])
        trig = 0   
    finally:
        if trig == 1:
            print("Collecting data for existing table: ", table_name)
            for i in range(len(x)):
                y = x.iloc[i+1]
                print(y)
                app_pop(table_name,y['state']) 
        elif trig == 0:
            print("Made it to iteration on new table.")
            for i in range(len(x)-1):
                y = x.iloc[i+1]
                print(y)
                app_pop(table_name,y['state'])    
        else:
            print("Nothing was done to anything and you have to re-do this code.")
