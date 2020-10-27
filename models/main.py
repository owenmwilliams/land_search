from est.calc import constr
from est.calc import comp_num
from est.plot import plotit
from datetime import datetime

StartWhile = datetime.now()
print(StartWhile)

x = comp_num.num_comps()
print(x)

plotit.showfig(x, 'radius', 'population', 'comps')

EndWhile = datetime.now()
print(EndWhile - StartWhile)