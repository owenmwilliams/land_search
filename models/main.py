from dtl.wrt.census_JSON_store import wrt_temp
from dtl.wrt.pop_table import wrt_pop
from datetime import datetime
from est.db.cur import con_cur
import psycopg2
from psycopg2 import sql

StartWhile = datetime.now()
print('*********************************', '\n')

#wrt_census("TestTableName")
wrt_pop("onlyuselowercase")

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)