from est.fltr import fltr_pd as ft
import pandas as pd

# get pop, value, share, air, parks_num
pop = ft.rank_low(ft.fltr_pop(0, 1000000), 'Pop')
print(pop)
value = ft.rank_low(ft.fltr_value(0, 1000000), 'Value')
print(value)
share = ft.rank_low(ft.fltr_share(0, 1000000), 'Share')
print(share)
air = ft.rank_high(ft.fltr_air(0, 10000000, 5), 'Air')
print(air)
parks = ft.rank_high(ft.fltr_parks(0, 10000, 5), 'Parks')
print(parks)

# join datasets
pv = pd.merge(pop, value, on='FIPS')
pvs = pd.merge(pv, share, on='FIPS')
pvsa = pd.merge(pvs, air, on='FIPS')
pvsap = pd.merge(pvsa, parks, on='FIPS')
print(pvsap)

# calc assessment (including weighted inputs)
pvsap['assessment'] = 0.2*pvsap['deciles_Pop'] + 0.2*pvsap['deciles_Value'] + 0.2*pvsap['deciles_Share'] + 0.2*pvsap['deciles_Air'] + 0.2*pvsap['deciles_Parks']
print(pvsap)

# rank & order counties
pvsap = pvsap.sort_values(by='assessment')
print(pvsap)

# drop decile columns & limit to top20
pvsap.drop(['deciles_Pop', 'deciles_Value', 'deciles_Share', 'deciles_Air', 'deciles_Parks'], axis=1, inplace=True)
pvsap = pvsap.iloc[:19,:]
print(pvsap)
