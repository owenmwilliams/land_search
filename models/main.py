from dtl.api.dtl_census import census_get, st_fips_get
from dtl.wrt.pop_table import wrt_pop, app_pop, census_loop
from datetime import datetime
from est.db.cur import con_cur
import psycopg2
from psycopg2 import sql
import pandas
import os

StartWhile = datetime.now()
print('*********************************', '\n')

# Appending works for smaller states
# Get ChunkedEncodingError from IncompleteRead and Connection broken with larger states (e.g., doesn't work for "04" - Arizona)
# Potential to stream with requests?

# wrt_pop("full_census")
# app_pop("full_census","04")
# x = st_fips_get()
# new_header = x.iloc[0]
# x = x[1:]
# x.columns = new_header
# x.drop_duplicates(subset=['state'], inplace=True)
# for i in range(len(x)):
#     y = x.iloc[i]
#     app_pop("census_table",y['state'])

census_loop("census_table")

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)
