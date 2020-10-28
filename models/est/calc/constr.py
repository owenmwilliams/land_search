from est.fltr import comps
from est.fltr import county_return


# iteration functions
def constr_itr(z):
    est = county_return.find_county()
    break_out = 0
    radius = 1
    population = 0.2

    while break_out <1:
        if radius < 4:
            x = comps.comp_find(est, radius, population)
            if len(x) >= z:
                break_out = 1
                return est, x, round(radius,2), round(population,2), len(x)
            else:
                radius = radius+0.5
        elif radius >= 4 and population < 4:
            x = comps.comp_find(est, radius, population)
            if len(x) >= z:
                break_out = 1
                return est, x, round(radius,2), round(population,2), len(x)
            else:
                population = population+0.2
        elif radius >= 4 and population >= 4 and radius < 10:
            x = comps.comp_find(est, radius, population)
            if len(x) >= z:
                break_out = 1
                return est, x, round(radius,2), round(population,2), len(x)
            else:
                radius = radius+1
        elif radius >= 10 and population >= 4 and population < 10:
            x = comps.comp_find(est, radius, population)
            if len(x) >= z:
                break_out = 1
                return est, x, round(radius,2), round(population,2), len(x)
            else:
                population = population+0.5
        elif radius >= 10 and population >= 10:
            x = []
            break_out = 1
            print('Not enough comps found.')
            return est, x, round(radius,2), round(population,2), len(x)
            