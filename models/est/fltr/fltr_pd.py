import psycopg2
from datetime import datetime
from psycopg2 import sql
from est.db.cur import con_cur
import pandas as pd

# return a list of counties based on population bounds
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
    print(pop_county)
    return pop_county

# return a list of counties based on value bounds
def fltr_value(minimum, maximum):
    cur, con = con_cur()
    cur.execute("""
            SELECT TRIM(county), TRIM(state), RIGHT(geo_id, 5), land_value_estimate
            FROM countydataset
            WHERE land_value_estimate <> 'Not enough comps.'
            AND land_value_estimate <> 'estimate'
            AND land_value_estimate::integer > {0}
            AND land_value_estimate::integer < {1};
        """.format(minimum, maximum))
    value_county = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS', 'Value'])
    value_county = value_county.astype({'Value':int})
    con.close()
    print(value_county)
    return value_county

# return a list of counties based on share bounds
def fltr_share(minimum, maximum):
    cur, con = con_cur()
    cur.execute("""
            SELECT TRIM(county), TRIM(state), RIGHT(geo_id, 5), land_share_estimate
            FROM countydataset
            WHERE land_value_estimate <> 'Not enough comps.'
            AND land_value_estimate <> 'estimate'
            AND land_share_estimate::decimal > {0}
            AND land_share_estimate::decimal < {1};
        """.format(minimum, maximum))
    share_county = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS', 'Share'])
    share_county = share_county.astype({'Share':float})
    con.close()
    print(share_county)
    return share_county

# return a list of counties based on commercial air traffic bounds
def fltr_air(minimum, maximum, radius):
    cur, con = con_cur()
    cur.execute("""
        WITH fnd AS (
            SELECT one.county, one.state, one.geoid, two.commercial_ops
            FROM countylatlong AS one
            CROSS JOIN placeairports AS two
            WHERE ST_Distance(one.geom, two.geom) < {0}
            ),
        agg AS (
            SELECT county, state, LPAD(geoid, 5, '0'), SUM(commercial_ops) AS comm_ops
            FROM fnd
            GROUP BY county, state, geoid
            )
        SELECT * FROM agg
        WHERE comm_ops > {1}
        AND comm_ops < {2}
        """.format(radius, minimum, maximum))
    air_county = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS', 'Air'])
    air_county = air_county.astype({'Air':int})
    con.close()
    print(air_county)
    return air_county

# return a list of counties based on parks bounds
def fltr_parks(minimum, maximum, radius):
    cur, con = con_cur()
    cur.execute("""
        WITH fnd AS (
            SELECT one.county, one.state, one.geoid, two.objectid
            FROM countylatlong AS one
            CROSS JOIN placerecreation AS two
            WHERE ST_Distance(one.geom, two.geom) < {0}
            ),
        agg AS (
            SELECT county, state, LPAD(geoid, 5, '0'), COUNT(objectid) AS num_parks
            FROM fnd
            GROUP BY county, state, geoid)
        SELECT * FROM agg
        WHERE num_parks > {1}
        AND num_parks < {2}
        """.format(radius, minimum, maximum))
    parks_county = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'FIPS', 'Parks'])
    parks_county = parks_county.astype({'Parks':int})
    con.close()
    print(parks_county)
    return parks_county

def rank_high(retDF, col_name):
    # popDF = pd.DataFrame([[10, 'A'], [7, 'A'], [9, 'A'], [8, 'C'], [4, 'B'], [2, 'B'], [5, 'D'], [1, 'D'], [2, 'B']], columns = ['Number', 'Letter'])    
    retDF = retDF
    retDF['deciles_{0}'.format(col_name)] = (pd.qcut(retDF[col_name], 10, labels = False) + 1) / 10
    return retDF

def rank_low(retDF, col_name):
    # popDF = pd.DataFrame([[10, 'A'], [7, 'A'], [9, 'A'], [8, 'C'], [4, 'B'], [2, 'B'], [5, 'D'], [1, 'D'], [2, 'B']], columns = ['Number', 'Letter'])    
    retDF = retDF
    retDF['deciles_{0}'.format(col_name)] = (10 - pd.qcut(retDF[col_name], 10, labels = False)) / 10
    return retDF
