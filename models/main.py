from dtl.dtl_census import census_get
from dtl.dtl_parks import parks_get
from datetime import datetime
from dtl.jprint import jprint

StartWhile = datetime.now()
print('*********************************', '\n')

x = parks_get()
jprint(x)

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)