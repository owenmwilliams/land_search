from dtl.wrt.pop_table import wrt_pop
from dtl.wrt.loc_table import wrt_loc
from dtl.api.dtl_census import census_get
from dtl.api.dtl_loc import shp_get
from dtl.api.dtl_icao import airports_get, departures_get
import pandas as pd
from datetime import datetime
from est.db.cur import con_cur
import psycopg2
from psycopg2 import sql

StartWhile = datetime.now()
print('*********************************', '\n')

#wrt_pop('new_table')

# wrt_loc('poly_table')

# x = airports_get()
# print(x)
# y = departures_get()
# print(y)

departures = pd.read_csv('icao_dep_data.csv')
locations = pd.read_csv('icao_lco_data.csv')

print(departures)
print(locations)

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)