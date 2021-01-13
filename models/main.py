import est.fltr.county_return as county_return
import est.fltr.search as search
import est.fltr.comps as comps
import est.calc.constr as constr
import est.calc.comp_assess as comp_assess
import dtl.wrt.wrt_hdfs as wrt_hdfs
from datetime import datetime
import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def find_lucky():
    x = county_return.random_county()
    print(x)

def find_state(state):
    array = county_return.state_search(state)
    print(array)

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

def assess(minimums, maximums, weights, radius):
    top20 = comp_assess.county_assess(minimums, maximums, weights, radius)
    print('*****')
    print(top20)
    print('#####')

def cluster_assess(min_pop, min_value, min_share, min_air, min_parks,\
    max_pop, max_value, max_share, max_air, max_parks,\
    weight_pop, weight_value, weight_share, weight_air, weight_parks,\
    radius_air, radius_parks):
    top20 = comp_assess.cluster(min_pop, min_value, min_share, min_air, min_parks,\
    max_pop, max_value, max_share, max_air, max_parks,\
    weight_pop, weight_value, weight_share, weight_air, weight_parks,\
    radius_air, radius_parks)
    print('*****')
    print(top20)
    print('#####')

def hdfs_dl(api_gateway):
    wrt_hdfs(api_gateway)
    print('Successfully updated %s' % api_gateway)
