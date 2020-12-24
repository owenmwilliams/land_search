import psycopg2
from datetime import datetime
from psycopg2 import sql
from est.db.cur import con_cur
import pandas as pd

# return a county based on population bounds
def fltr_pop(minimum, maximum):
    cur, con = con_cur()
    cur.execute("""
            SELECT TRIM(county), TRIM(state), RIGHT(geo_id, 5), population
            FROM countydataset
            WHERE population::integer > {0}
            AND population::integer < {1};
        """.format(minimum, maximum))
    pop_county = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS', 'Pop'])
    con.close()
    return pop_county

# TODO: All these functions need to remove any results that say 'Not enough comps.'

def fltr_value(minimum, maximum):
    cur, con = con_cur()
    cur.execute("""
            SELECT TRIM(county), TRIM(state), RIGHT(geo_id, 5), land_value_estimate
            FROM countydataset
            WHERE land_value_estimate <> 'Not enough comps.'
            AND land_value_estimate::integer > {0}
            AND land_value_estimate::integer < {1};
        """.format(minimum, maximum))
    value_county = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS', 'Value'])
    con.close()
    return value_county

def fltr_share(minimum, maximum):
    cur, con = con_cur()
    cur.execute("""
            SELECT TRIM(county), TRIM(state), RIGHT(geo_id, 5), land_share_estimate
            FROM countydataset
            WHERE land_value_estimate <> 'Not enough comps.'
            AND land_share_estimate::integer > {0}
            AND land_share_estimate::integer < {1};
        """.format(minimum, maximum))
    value_county = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS', 'Share'])
    con.close()
    return value_county

def fltr_air(minimum, maximum, radius):
    cur, con = con_cur()
    cur.execute("""
        WITH agg AS (
            SELECT one.county, one.state, two.commercial_ops
            FROM countylatlong AS one
            CROSS JOIN placeairports AS two
            WHERE ST_Distance(one.geom, two.geom) < {0}
            )
        SELECT county, state, LPAD(geoid, 5, '0'), SUM(commercial_ops) AS comm_ops
        FROM agg
        GROUP BY county, state
        WHERE comm_ops > {1}
        AND comm_ops < {2}
        """.format(radius, minimum, maximum))
    value_air = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS', 'Air'])
    con.close()
    return value_county

def rank(retDF, col_name):
    # popDF = pd.DataFrame([[10, 'A'], [7, 'A'], [9, 'A'], [8, 'C'], [4, 'B'], [2, 'B'], [5, 'D'], [1, 'D'], [2, 'B']], columns = ['Number', 'Letter'])    
    retDF = retDF
    retDF['deciles_{0}'.format(col_name)] = (pd.qcut(retDF[col_name], 10, labels = False) + 1) / 10
    return retDF
