from est.calc import constr
from est.calc import comp_num
from est.plot import plotit
import numpy as np
from est.calc import outlier
from est.db import updates
from est.db.cur import con_cur
import psycopg2


def calc(numb):
    
    # GET THE DATA FOR COMPS
    subj_cty, comp_cty, radius, population, num_comps = constr.constr_itr(numb)
    print('County being assessed: ', subj_cty[0][0], ', ', subj_cty[0][1], '\n')

    # APPEND THE CONSTRAINTS USED TO DATABASE
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
    updates.update_comps(str(ctys), subj_cty)

    # UPDATE THE LAND VALUE IN THE DATABASE
    if len(ctys) > 0:
        lv = []
        for i in range(len(comp_cty)):
            lv.append(comp_cty[i][2])
        updates.update_lv(round(np.mean(lv)), subj_cty)
    else:
        cur, con = con_cur()
        cur.execute("""
            UPDATE county_population_csv cpc
                SET land_value_estimate = 'Not enough comps.'
                    WHERE trim(cpc.state) = %(st)s
                    AND trim(cpc.county) = %(cty)s
                    AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
                    """, {'st':str(subj_cty[0][1].strip()), 'cty':str(subj_cty[0][0].strip())})
        con.commit()

    # UPDATE THE LAND VALUE AS PERC OF TOTAL VALUE IN THE DATABASE
    if len(ctys) > 0:
        shr = []
        for i in range(len(comp_cty)):
            shr.append(comp_cty[i][3])
        updates.update_shr(round(np.mean(shr), 3), subj_cty)
        