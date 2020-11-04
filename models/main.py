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

# Appending works for smaller states
# Get ChunkedEncodingError from IncompleteRead and Connection broken with larger states (e.g., doesn't work for "04" - Arizona)
# Potential to stream with requests?

# wrt_pop("full_census")
app_pop("full_census","30")

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)