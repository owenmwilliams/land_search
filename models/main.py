import est.fltr.county_return as county_return
from datetime import datetime
import pandas as pd
import os


def find_lucky():

    StartWhile = datetime.now()
    print('*********************************', '\n')

    x = county_return.random_county()
    print(x)

    EndWhile = datetime.now()
    print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)

def find_state(state):

    StartWhile = datetime.now()
    print('*********************************', '\n')

    x = county_return.state_search(state)
    pd.set_option('display.max_rows', None)
    print(x)

    EndWhile = datetime.now()
    print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)

# census_loop("census_table")