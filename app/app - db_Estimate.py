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
            SELECT * FROM est_LandValue(%s, 0.2, 5, %s, %s)
        """ {break_out, query_state[1], query_state[0]})
        comp_states = cur.fetchall()
        if not comp_states:
            print('Not enough comps, increasing radius')
            break_out = break_out + 0.5
        else:
            print('Sufficient comps found, updating pop table')
            cur.execute("""
                UPDATE county_population_csv cpc
                    SET comps = %s
                    FROM (SELECT STRING_AGG(concat_list, '; ') FROM concat_list) AS subquery
                    WHERE trim(cpc.state) = %s
                    AND cpc.county = %s
                    AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
            """ {comp_states[    query_state[1], query_state[0]}
# set up loop to find the most accurate estimate (relaxing pop)

# set up loop to find the most accurate estimate (relaxing comps)


con.close
    
