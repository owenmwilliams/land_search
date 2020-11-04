from dtl.wrt.pop_table import wrt_pop
from dtl.wrt.loc_table import wrt_loc
from dtl.api.dtl_census import census_get
from dtl.api.dtl_loc import shp_get
from datetime import datetime
from est.db.cur import con_cur
import psycopg2
from psycopg2 import sql

StartWhile = datetime.now()
print('*********************************', '\n')

#wrt_pop('new_table')

wrt_loc('poly_table')



EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)