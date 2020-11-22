import est.fltr.county_return as county_return
import est.fltr.comps as comps
from datetime import datetime
import pandas as pd
import os


def find_lucky():
    x = county_return.random_county()
    return x

def find_state(state):
    array = county_return.state_search(state)
    return array

def params_estimate(population, radius, cty_fips):
    print('*********************************************************')
    county, state = county_return.fips_2_county(cty_fips)
    print(county)
    print(state)
    comparables = comps.find_comps(state, county, radius, population)
    print('*********************************************************')
    print(comparables)



# # census_loop("census_table")