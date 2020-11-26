import psycopg2
from datetime import datetime
from psycopg2 import sql
from est.fltr import county_return
from est.db.cur import con_cur
import numpy as np
import pandas as pd

def comp_find(est, a, b):
    temp1 = est
    temp2 = np.array(temp1[0])
    county = temp2[0].strip()
    state = temp2[1].strip()

    cur, con = con_cur()
    cur.execute("""
                SELECT comp_st, comp_cty, comp_lv, comp_perc FROM est_LandValue(%s, %s, %s, %s) 
            """, (a, b, state, county))
    comp_states = cur.fetchall()
    con.close()
    return(comp_states)

def find_comps(state, county, radius, population):
    cur, con = con_cur()
    cur.execute("""
                SELECT comp_st, comp_cty, comp_lv, comp_perc FROM est_LandValue(%s, %s, %s, %s) 
            """, (radius, population, state, county))
    comp_states = pd.DataFrame(cur.fetchall(), columns = ['State', 'County', 'Land Value', 'Perc Land Value'])
    con.close()
    return(comp_states)
