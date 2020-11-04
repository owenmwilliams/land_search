from dtl.api.dtl_census_copy import census_get
from dtl.wrt.pop_table import wrt_pop
from datetime import datetime
from est.db.cur import con_cur
import psycopg2
from psycopg2 import sql
import pandas
import os

StartWhile = datetime.now()
print('*********************************', '\n')

wrt_pop("dat_full_census")

# x = census_get()
# print(x)
# print(len(x))

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)