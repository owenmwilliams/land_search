import psycopg2
from datetime import datetime
from psycopg2 import sql

# returning a single county without an existing land value estimate
def find_county():
    con = psycopg2.connect(database='owenwilliams', host="localhost", port="5434")
    cur = con.cursor()
    cur.execute("""
            SELECT county, state
            FROM county_population_csv cpc 
                WHERE land_value_estimate = 'estimate' 
                AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'
            LIMIT 1;
        """)
    cty_test = cur.fetchall()
    return cty_test