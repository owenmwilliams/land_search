from est.calc import constr
from est.calc import comp_num
from est.plot import plotit
from datetime import datetime
import numpy as np
from est.calc import outlier
from est.db import updates

StartWhile = datetime.now()
print('*********************************', '\n')

#x = comp_num.num_comps()
#print(x)
#plotit.showfig(x, 'radius', 'population', 'comps')

# GET THE DATA FOR COMPS

subj_cty, comp_cty, radius, population, num_comps = constr.constr_itr(10)

print('County being assessed: ', subj_cty[0][0], ', ', subj_cty[0][1], '\n')

# APPEND THE CONSTRAINTS USED TO DATABASE

print(' Radius constraint used: ', radius, '\n', 'Population constraint used: ', population, '\n', 'Number of comps found: ', num_comps, '\n')
x = []
x.append(radius)
x.append(population)
x.append(num_comps)
updates.update_constr(x, subj_cty)

# APPEND THE COMPS USED TO DATABASE

ctys = []
for i in range(len(comp_cty)):
    ctys.append(comp_cty[i][0])
    ctys.append(comp_cty[i][1])

print('Comparison counties:')
i = 0
while i < len(ctys):
    print(ctys[i], ', ', ctys[i+1])
    i = i+2
print('\n')

updates.update_comps(str(ctys), subj_cty)

# UPDATE THE LAND VALUE IN THE DATABASE

lv = []
for i in range(len(comp_cty)):
    lv.append(comp_cty[i][2])
print('Average land value: ', np.mean(lv), '\n')

updates.update_lv(round(np.mean(lv)), subj_cty)

# UPDATE THE LAND VALUE AS PERC OF TOTAL VALUE IN THE DATABASE

shr = []
for i in range(len(comp_cty)):
    shr.append(comp_cty[i][3])
print('Average value percent in land: ', np.mean(shr), '\n')

updates.update_shr(round(np.mean(shr), 3), subj_cty)

# ADD CONFIDENCE CALCULATION TO DATABASE POPULATION TABLE

conf1 = outlier.detect_outlier(lv)
print(len(conf1), len(conf1)/len(lv))

conf2 = np.std(lv)
print(conf2, np.mean(lv), (conf2-np.mean(lv))/np.mean(lv))

EndWhile = datetime.now()
print('Time for calculation: ', EndWhile - StartWhile)