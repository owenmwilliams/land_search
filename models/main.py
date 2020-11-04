from dtl.api.dtl_census import census_get
from dtl.wrt.pop_table import wrt_pop, app_pop
from datetime import datetime
from est.db.cur import con_cur
import psycopg2
from psycopg2 import sql
import pandas
import os

StartWhile = datetime.now()
print('*********************************', '\n')

# wrt_pop("full_census")
app_pop("full_census")

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)