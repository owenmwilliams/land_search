import est.fltr.county_return as county_return
import est.fltr.search as search
import est.fltr.comps as comps
import est.calc.constr as constr
from datetime import datetime
import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def find_lucky():
    x = county_return.random_county()
    return x

def find_state(state):
    array = county_return.state_search(state)
    return array

def params_estimate(population, radius, cty_fips):
    print('*****')
    county, state = county_return.fips_2_county(cty_fips)
    print(county, state)
    print('#####')
    comparables = comps.find_comps(state, county, radius, population)
    print('*****')
    print(comparables)
    print('#####')
    print('*****')
    print(comparables['Land Value'].describe())
    print('#####')
    print('*****')
    print(comparables['Perc Land Value'].astype('float64').describe())
    print('#####')

def comps_estimate(comp_number, cty_fips):
    print('*****')
    county, state = county_return.fips_2_county(cty_fips)
    print(county, state)
    print('#####')
    comparables, radius, population, comps = constr.constr_itr(state, county, comp_number)
    if len(comparables) == 1:
        print('*****')
        print('Not enough comps found.')
        print('#####')
    else:
        print('*****')
        print(comps, 'comparable counties within ', radius, 'degrees lat / long and +/-', population, 'population.')
        print('#####')
        print('*****')
        print(comparables)
        print('#####')
        print('*****')
        print(comparables['Land Value'].describe())
        print('#####')
        print('*****')    
        print(comparables['Perc Land Value'].astype('float64').describe())
        print('#####')

def search_all(value, share, pop):
    top20 = search.search_all(value, share, pop)
    print('*****')
    print(top20)
    print('#####')

def search_complex(value, share, pop, air_prox, parks_prox, parks_num):
    top20 = search.search_complex(value, share, pop, air_prox, parks_prox, parks_num)
    print('*****')
    print(top20)
    print('#####')

# # census_loop("census_table")