from est.fltr import fltr_pd as ft
import pandas as pd
import yaml

def county_assess(doc_path):
    # pull values from YAML file (TODO: make local or cluster)
    print(doc_path)
    stream = open(doc_path)
    boundaries = yaml.load_all(stream, Loader=yaml.FullLoader)
    for data in boundaries:
        for j, k in data.items():
            if j == 'minimums':
                minimums = k
            elif j == 'maximums':
                maximums = k
            elif j == 'weights':
                weights = k
            elif j == 'radius':
                radius = k
    
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
    pvsap['assessment'] = weight_list[0]*pvsap['deciles_Pop'] + weight_list[1]*pvsap['deciles_Value'] + weight_list[2]*pvsap['deciles_Share'] + weight_list[3]*pvsap['deciles_Air'] + weight_list[4]*pvsap['deciles_Parks']

    # rank & order counties
    pvsap = pvsap.sort_values(by='assessment', ascending=False)

    # drop decile columns & limit to top20
    pvsap = pvsap[['assessment','County', 'State','FIPS','Pop', 'Value', 'Share', 'Air', 'Parks']]
    pvsap = pvsap.iloc[:20,:]
    return pvsap

def other_function():
    print('Other function')
    