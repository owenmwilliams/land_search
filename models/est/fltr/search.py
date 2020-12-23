import psycopg2
from datetime import datetime
from psycopg2 import sql
from est.fltr import county_return
from est.db.cur import con_cur
import numpy as np
import pandas as pd

def search_all(value, share, population):
    cur, con = con_cur()
    cur.execute("""
                SELECT county, state, population, land_value_estimate, land_share_estimate 
                FROM countydataset
                WHERE land_value_estimate <> 'Not enough comps.' 
                AND land_value_estimate::integer < {0}
                AND land_share_estimate::decimal < {1}
                AND population::integer < {2}
                ORDER BY land_value_estimate ASC
                LIMIT 20;
            """.format(int(value), float(share), int(population)))
    search_counties = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'Pop', 'Value', 'Share'])
    con.close()
    return(search_counties)

# TODO: UPDATE FUNCTION TO SELECT FROM COUNTYDATASET WHERE NOT 'NOT ENOUGH COMPS' PER ABOVE

def search_complex(value, share, pop, air_prox, parks_prox, parks_num):
    cur, con = con_cur()
    # cur.execute("""
    #             SELECT comp_st, comp_cty, comp_lv, comp_perc FROM lookup_YrCostPopShareAirPark(cursor,{0},{1},{2},{3},{4},{5},{6})
    #             LIMIT 20;
    #             """.format('2018', population, value, share, air_prox, parks_prox, parks_num))
    cur.execute("""
                WITH cte AS (
				    SELECT one.county, one.state, two.loc_id, two.commercial_ops, ST_Distance(one.geom, two.geom) as dist
					FROM countylatlong as one
					CROSS JOIN placeairports as two
					WHERE ST_Distance(one.geom, two.geom) < {0}
			    ), sort AS (
				    SELECT *, row_number() OVER (PARTITION BY state, county ORDER BY dist) as rn
					FROM cte
			    ), clp AS (
				    SELECT three.county, three.state, four.gnis_id, four.unit_name, four.lat, four.long, ST_Distance(three.geom, four.geom) AS dist 
					FROM countylatlong AS three
					CROSS JOIN placerecreation AS four
					WHERE ST_Distance(three.geom, four.geom) < {1}
			    ), sortp AS (
				    SELECT distinct(county), count(*) AS num_parks, state
					FROM clp
					WHERE county IS NOT NULL
					GROUP BY county, state
			    )
			    SELECT clc.county, clc.state, clc.land_value_estimate, clc.land_share_estimate, clc.population, sort.loc_id, sortp.num_parks
				FROM countydataset clc
				JOIN sort
					ON trim(sort.county) = trim(clc.county) 
					AND trim(sort.state) = trim(clc.state)
				JOIN sortp
					ON trim(sortp.county) = trim(clc.county) 
					AND trim(sortp.state) = trim(clc.state)
				WHERE clc.land_value_estimate <> 'Not enough comps.' 
					AND clc.population < {2}
					AND clc.land_value_estimate < {3}
					AND clc.land_share_estimate < {4}
					AND sort.rn = 1
					AND sortp.num_parks > {5}
				ORDER BY clc.land_value_estimate ASC 
                LIMIT 20;
                """.format(air_prox, parks_prox, pop, value, share, parks_num))

    search_counties = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'Value', 'Share', 'Pop', 'Air', 'Parks'])
    con.close()
    return(search_counties)
