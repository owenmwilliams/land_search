from est.fltr import fltr_pd as ft
import pandas as pd
import yaml

def county_assess(minimums, maximums, weights, radius):  
    # get pop, value, share, air, parks_num
    pop = ft.rank_low(ft.fltr_pop(minimums['pop'], maximums['pop']), 'Pop')
    value = ft.rank_low(ft.fltr_value(minimums['value'], maximums['value']), 'Value')
    share = ft.rank_low(ft.fltr_share(minimums['share'], maximums['share']), 'Share')
    air = ft.rank_high(ft.fltr_air(minimums['air'], maximums['air'], radius['air']), 'Air')
    parks = ft.rank_high(ft.fltr_parks(minimums['parks'], maximums['parks'], radius['parks']), 'Parks')

    # join datasets
    pv = pd.merge(pop, value, on='FIPS')
    pvs = pd.merge(pv, share, on='FIPS')
    pvsa = pd.merge(pvs, air, on='FIPS')
    pvsap = pd.merge(pvsa, parks, on='FIPS')

    # calc assessment (including weighted inputs)
    pvsap['assessment'] = weights['pop']*pvsap['deciles_Pop'] + weights['value']*pvsap['deciles_Value'] + weights['share']*pvsap['deciles_Share'] + weights['air']*pvsap['deciles_Air'] + weights['parks']*pvsap['deciles_Parks']

    # rank & order counties
    pvsap = pvsap.sort_values(by=['assessment', 'County'], ascending=False)

    # drop decile columns & limit to top20
    pvsap = pvsap[['assessment','County', 'State','FIPS','Pop', 'Value', 'Share', 'Air', 'Parks']]
    pvsap = pvsap.iloc[:20,:]
    return pvsap

def cluster(min_pop, min_value, min_share, min_air, min_parks,\
    max_pop, max_value, max_share, max_air, max_parks,\
    weight_pop, weight_value, weight_share, weight_air, weight_parks,\
    radius_air, radius_parks):
    
    # get pop, value, share, air, parks_num
    pop = ft.rank_low(ft.fltr_pop(min_pop, max_pop), 'Pop')
    value = ft.rank_low(ft.fltr_value(min_value, max_value), 'Value')
    share = ft.rank_low(ft.fltr_share(min_share, max_share), 'Share')
    air = ft.rank_high(ft.fltr_air(min_air, max_air, radius_air), 'Air')
    parks = ft.rank_high(ft.fltr_parks(min_parks, max_parks, radius_parks), 'Parks')

    # join datasets
    pv = pd.merge(pop, value, on='FIPS')
    pvs = pd.merge(pv, share, on='FIPS')
    pvsa = pd.merge(pvs, air, on='FIPS')
    pvsap = pd.merge(pvsa, parks, on='FIPS')

    # calc assessment (including weighted inputs)
    pvsap['assessment'] = weight_pop*pvsap['deciles_Pop'] + weight_value*pvsap['deciles_Value'] + weight_share*pvsap['deciles_Share'] + weight_air*pvsap['deciles_Air'] + weight_parks*pvsap['deciles_Parks']

    # rank & order counties
    pvsap = pvsap.sort_values(by=['assessment', 'County'], ascending=False)

    # drop decile columns & limit to top20
    pvsap = pvsap[['assessment','County', 'State','FIPS','Pop', 'Value', 'Share', 'Air', 'Parks']]
    pvsap = pvsap.iloc[:20,:]
    return pvsap
    