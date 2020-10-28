from est.calc import comp_calc
import numpy as np
from datetime import datetime
from est.calc import kill_whiletruetest
from est.fltr.end_list import at_end


StartWhile = datetime.now()
print('*********************************', '\n')

i = 0
while True:
    try:
        at_end(i)
        print(i, '________________________________')
        comp_calc.calc(10)
        i = i+1
    except ValueError:
        print('End of list...')

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)