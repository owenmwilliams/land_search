from dtl.dtl_census import census_get
from dtl.dtl_parks import parks_get
from dtl.dtl_loc import shp_get
from datetime import datetime
from dtl.jprint import jprint
import pandas as pd
import json

StartWhile = datetime.now()
print('*********************************', '\n')

#x = parks_get()
#print(x)

#y = census_get()
#print(y)

z = shp_get()
print(z)

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)