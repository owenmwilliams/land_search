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
            FROM countydataset cpc 
                WHERE land_value_estimate = 'estimate' 
                AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'
                AND state IS NOT NULL
                AND county IS NOT NULL
            LIMIT 1;
        """)
    cty_test = cur.fetchall()
    con.close()
    return cty_test

# return a random county from county_population table
def random_county():
    cur, con = con_cur()
    cur.execute("""
            SELECT TRIM(county), TRIM(state), RIGHT(geo_id, 5)
            FROM countydataset
            TABLESAMPLE BERNOULLI(.01)
            LIMIT 1;
        """)
    cty_test = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS'])
    con.close()
    return cty_test

# return all counties within a specific state from county_population table
def state_search(state):
    cur, con = con_cur()
    cur.execute("""
            SELECT DISTINCT TRIM(county), TRIM(state), RIGHT(geo_id, 5)
            FROM countydataset
            WHERE TRIM(state) = '%s';
        """ % state)
    cty_array = pd.DataFrame(cur.fetchall(), columns = ['County','State','FIPS'])
    con.close()
    return cty_array

# return the county and state from a FIPS code
def fips_2_county(FIPS):
    cur, con = con_cur()
    cur.execute("""
            SELECT DISTINCT TRIM(county), TRIM(state)
            FROM countydataset
            WHERE RIGHT(geo_id, 5) = LPAD(%s::VARCHAR, 5, '0')
            LIMIT 1;
        """ % FIPS)
    array = pd.DataFrame(cur.fetchall(), columns = ['County', 'State'])
    county = array['County'][0]
    state = array['State'][0]
    con.close()
    return county, state
