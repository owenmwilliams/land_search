import psycopg2
from est.db.cur import con_cur

def at_end(a):
    cur = con_cur()
    cur.execute("""
            SELECT *
            FROM county_population_csv cpc 
                WHERE land_value_estimate = 'estimate' 
                AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'
            LIMIT 1;
        """)
    end_test = cur.fetchall()
    if len(end_test) > 0:
        return True
    else:
        return False