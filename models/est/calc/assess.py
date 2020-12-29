from est.fltr import fltr_pd as ft
import pandas as pd

def county_assess(minmax_list, weight_list, air_radius, parks_radius):
    minmax_list = [0,1000000,0,1000000,0,1000000,0,10000000,0,10000]
    weight_list = [0.2, 0.2, 0.2, 0.2, 0.2]
    
    # get pop, value, share, air, parks_num
    pop = ft.rank_low(ft.fltr_pop(minmax_list[0], minmax_list[1]), 'Pop')
    value = ft.rank_low(ft.fltr_value(minmax_list[2], minmax_list[3]), 'Value')
    share = ft.rank_low(ft.fltr_share(minmax_list[4], minmax_list[5]), 'Share')
    air = ft.rank_high(ft.fltr_air(minmax_list[6], minmax_list[7], air_radius), 'Air')
    parks = ft.rank_high(ft.fltr_parks(minmax_list[8], minmax_list[9], parks_radius), 'Parks')

    # join datasets
    pv = pd.merge(pop, value, on='FIPS')
    pvs = pd.merge(pv, share, on='FIPS')
    pvsa = pd.merge(pvs, air, on='FIPS')
    pvsap = pd.merge(pvsa, parks, on='FIPS')

    # calc assessment (including weighted inputs)
    pvsap['assessment'] = weight_list[0]*pvsap['deciles_Pop'] + weight_list[1]*pvsap['deciles_Value'] + weight_list[2]*pvsap['deciles_Share'] + weight_list[3]*pvsap['deciles_Air'] + weight_list[4]*pvsap['deciles_Parks']

    # rank & order counties
    pvsap = pvsap.sort_values(by='assessment', ascending=False)

    # drop decile columns & limit to top20
    pvsap = pvsap[['assessment','County', 'State','FIPS','Pop', 'Value', 'Share', 'Air', 'Parks']]
    pvsap = pvsap.iloc[:20,:]
    return pvsap
