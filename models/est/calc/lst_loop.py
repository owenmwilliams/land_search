from est.calc import comp_calc
from est.fltr.end_list import at_end


def lst_loop(cmps):
    i = 0
    x = at_end(i)
    while x == 1:
        print(i, '________________________________')
        comp_calc.calc(cmps)
        i = i+1
        x = at_end(i)
    else:
        print('End of list...')
