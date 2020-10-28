from est.calc.lst_loop import lst_loop
from datetime import datetime

StartWhile = datetime.now()
print('*********************************', '\n')

lst_loop(5)

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)