import psycopg2
from datetime import datetime
from psycopg2 import sql
from est.db.cur import con_cur
import pandas as pd

# returning a single county WITHOUT an existing land value estimate
def find_county():
    cur, con = con_cur()
    cur.execute("""
            SELECT county, state
            FROM county_population_csv cpc 
                WHERE land_value_estimate = 'estimate' 
                AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'
                AND state IS NOT NULL
                AND county IS NOT NULL
            LIMIT 1;
        """)
    cty_test = cur.fetchall()
    con.close()
    return cty_test

def random_county():
    cur, con = con_cur()
    cur.execute("""
            SELECT TRIM(county), TRIM(state), RIGHT(geo_id, 5)
            FROM county_population_csv
            TABLESAMPLE BERNOULLI(.01)
            LIMIT 1;
        """)
    cty_test = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS'])
    con.close()
    return cty_test

def state_search(state):
    cur, con = con_cur()
    cur.execute("""
            SELECT DISTINCT TRIM(county), TRIM(state), RIGHT(geo_id, 5)
            FROM county_population_csv
            WHERE TRIM(state) = '%s';
        """ % state)
    cty_array = pd.DataFrame(cur.fetchall(), columns = ['County','State','FIPS'])
    con.close()
    return cty_array
