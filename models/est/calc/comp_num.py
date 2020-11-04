from est.fltr import comps
from est.fltr import county_return
import numpy as np
import pandas as pd


# function to cycle through pop & dist variables and return number of comps
def num_comps():
    radius = 0
    population = 0.5
    array = np.array([[0, 0, 0]])

    while radius <= 20:
        while population <= 10:
            x = comps.comp_find(radius, population)
            array = np.append(array, [[radius, population, len(x)]], axis=0)
            population = population+0.5
        radius = radius + 1
        population = 0.5
    
    data_frame = pd.DataFrame(array, columns = ['radius', 'population', 'comps'])
    return data_frame
    