import psycopg2
from datetime import datetime
from psycopg2 import sql
from fltr import county_return
from est import cur
import numpy as np

temp1 = find_county()
temp2 = np.array(temp1[0])
county = temp2[0].strip()
state = temp2[1].strip()
print(county)
print(state)

cur = con_cur()
cur.execute("""
            SELECT comp_st, comp_cty FROM est_LandValue(10, 3, 5, %s, %s) 
        """, (state, county))
comp_states = cur.fetchall()
print(comp_states)