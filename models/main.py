from dtl.wrt.pop_table import wrt_pop
from datetime import datetime
from est.db.cur import con_cur
import psycopg2
from psycopg2 import sql

StartWhile = datetime.now()
print('*********************************', '\n')

wrt_pop('new_table')

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)