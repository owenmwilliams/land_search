import psycopg2
from datetime import datetime
from psycopg2 import sql
from county_return import find_county
import numpy as np

temp1 = find_county()
temp2 = np.array(temp1[0])
county = temp2[0].strip()
state = temp2[1].strip()
print(county)
print(state)

con = psycopg2.connect(database='owenwilliams', host="localhost", port="5434")
cur = con.cursor()
cur.execute("""
            SELECT * FROM est_LandValue(10, 3, 5, %s, %s) 
        """, (state, county))
comp_states = cur.fetchall()
print(comp_states)