import psycopg2
from datetime import datetime
from psycopg2 import sql
from est.db.cur import con_cur

# returning a single county without an existing land value estimate
def find_county():
    cur = con_cur()
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
    return cty_test