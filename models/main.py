import est.fltr.county_return as county_return
import est.fltr.comps as comps
import est.calc.constr as constr
from datetime import datetime
import pandas as pd
import os

pd.set_option('display.max_rows', None)

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
    print(comparables['Land Value'].describe())
    print(comparables['Perc Land Value'].astype('float64').describe())

def comps_estimate(comp_number, cty_fips):
    print('*********************************************************')
    county, state = county_return.fips_2_county(cty_fips)
    print(county)
    print(state)
    comparables, radius, population, comps = constr.constr_itr(state, county, comp_number)
    print('*********************************************************')
    print(comps, 'comparable counties within ', radius, 'degrees lat / long and +/-', population, 'population.')
    print(comparables)
    print(comparables.describe())

# # census_loop("census_table")