from dtl.api.dtl_census import census_get, st_fips_get
from dtl.wrt.pop_table import wrt_pop, app_pop, census_loop
from datetime import datetime
from est.db.cur import con_cur
import psycopg2
from psycopg2 import sql
import pandas as pd
import os

StartWhile = datetime.now()
print('*********************************', '\n')

census_loop("census_table")

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)
