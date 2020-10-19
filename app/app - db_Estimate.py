import psycopg2
from datetime import datetime
from psycopg2 import sql
from operator import itemgetter

# timing start
StartTime = datetime.now()

# connecting to the right database
con = psycopg2.connect(database='owenwilliams', host="localhost", port="5434")
Time1 = datetime.now()-StartTime
print("Database opened successfully: ", Time1)

# setting up a cursor
cur = con.cursor()

# set a break to leave the loop
break_out = 1

# set up loop to find the most accurate estimate (relaxing geo)
while break_out < 10:
    cur.execute("""
        SELECT county, state
        FROM county_population_csv cpc 
            WHERE land_value_estimate = 'estimate' 
            AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'
        LIMIT 1;
    """)
    query_state = cur.fetchall()
    if not query_state:
        break
    else:
        cur.execute("""
            SELECT * FROM est_LandValue(1, 0.2, 5, %s, %s)
        """ {query_state[1], query_state[0]})
    
# set up loop to find the most accurate estimate (relaxing pop)

# set up loop to find the most accurate estimate (relaxing comps)


con.close
    
