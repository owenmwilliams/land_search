import est.fltr.county_return as county_return
from datetime import datetime
import os


def lucky():

    StartWhile = datetime.now()
    print('*********************************', '\n')

    x = county_return.random_county()
    print(x)

    EndWhile = datetime.now()
    print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)


# census_loop("census_table")