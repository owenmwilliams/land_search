from est.fltr import comps
from est.fltr import county_return


# iteration functions
def constr_itr(state, county, comp_number):
    break_out = 0
    radius = 1
    population = 0.2
    comp_number = int(comp_number)

    while break_out <1:
        if radius < 4:
            array = comps.find_comps(state, county, radius, population)
            if len(array) >= comp_number:
                break_out = 1
                return array, round(radius,2), round(population,2), len(array)
            else:
                radius = radius+0.5
        elif radius >= 4 and population < 4:
            array = comps.find_comps(state, county, radius, population)
            if len(array) >= comp_number:
                break_out = 1
                return array, round(radius,2), round(population,2), len(array)
            else:
                population = population+0.2
        elif radius >= 4 and population >= 4 and radius < 10:
            array = comps.find_comps(state, county, radius, population)
            if len(array) >= comp_number:
                break_out = 1
                return array, round(radius,2), round(population,2), len(array)
            else:
                radius = radius+1
        elif radius >= 10 and population >= 4 and population < 10:
            array = comps.find_comps(state, county, radius, population)
            if len(array) >= comp_number:
                break_out = 1
                return array, round(radius,2), round(population,2), len(array)
            else:
                population = population+0.5
        elif radius >= 10 and population >= 10:
            array = ['Not enough comps found.']
            break_out = 1
            print('Not enough comps found.')
            return array, round(radius,2), round(population,2), len(array)
