import est.fltr.county_return as county_return
from datetime import datetime
import pandas as pd
import os


def find_lucky():
    x = county_return.random_county()
    print(x)

def find_state(state):
    array = county_return.state_search(state)
    return array

# census_loop("census_table")