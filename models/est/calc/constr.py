from est.fltr import comps
from est.fltr import county_return


# iteration functions
def constr_itr(z):
    x = county_return.find_county()
    break_out = 0
    radius = 1
    population = 0.2
    
    while break_out <1:
        if radius < 4:
            x = comps.comp_find(radius, population)
            if len(x) >= z:
                break_out = 1
                print('Radius was: ', radius, ' Population was: ', round(population), ' Number of comps was: ', len(x))
                for i in range(len(x)):
                    print(x[i])
            else:
                radius = radius+0.5
        elif radius >= 4 and population < 4:
            x = comps.comp_find(radius, population)
            if len(x) >= z:
                break_out = 1
                print('Radius was:', radius, ' Population was:', round(population), ' Number of comps was:', len(x))
                for i in range(len(x)):
                    print(x[i])
            else:
                population = population+0.2
        elif radius >= 4 and population >= 4:
            x = comps.comp_find(radius, population)
            if len(x) >= z:
                break_out = 1
                print('Radius was:', radius, ' Population was:', round(population), ' Number of comps was:', len(x))
                for i in range(len(x)):
                    print(x[i])
            else:
                radius = radius+0.5
        elif radius >= 30:
            break_out = 1
            print('Not enough comps found.')