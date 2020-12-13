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
    search_counties = pd.DataFrame(cur.fetchall(), columns = ['County', 'State', 'Population', 'Value', 'Share'])
    con.close()
    return(search_counties)
