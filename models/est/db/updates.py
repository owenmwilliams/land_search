import psycopg2

def update_constr(b, a):
    con = psycopg2.connect(database='owenwilliams', host="localhost", port="5434")
    cur = con.cursor()
    cur.execute("""
        UPDATE county_population_csv cpc
            SET est_base = %(str)s
                WHERE trim(cpc.state) = %(st)s
                AND trim(cpc.county) = %(cty)s
                AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
                """, {'str':b, 'st':str(a[0][1].strip()), 'cty':str(a[0][0].strip())})
    con.commit()
    print('Database updated, check: ', str(a[0][0].strip()), ', ', str(a[0][1].strip()), 'on column est_base value: ', str(b), '\n')


def update_comps(b, a):
    con = psycopg2.connect(database='owenwilliams', host="localhost", port="5434")
    cur = con.cursor()
    cur.execute("""
        UPDATE county_population_csv cpc
            SET comps = %(str)s
                WHERE trim(cpc.state) = %(st)s
                AND trim(cpc.county) = %(cty)s
                AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
                """, {'str':b, 'st':str(a[0][1].strip()), 'cty':str(a[0][0].strip())})
    con.commit()
    print('Database updated, check: ', str(a[0][0].strip()), ', ', str(a[0][1].strip()), 'on column comps value: ', str(b), '\n')

def update_lv(b, a):
    con = psycopg2.connect(database='owenwilliams', host="localhost", port="5434")
    cur = con.cursor()
    cur.execute("""
        UPDATE county_population_csv cpc
            SET land_value_estimate = %(str)s
                WHERE trim(cpc.state) = %(st)s
                AND trim(cpc.county) = %(cty)s
                AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
                """, {'str':b, 'st':str(a[0][1].strip()), 'cty':str(a[0][0].strip())})
    con.commit()
    print('Database updated, check: ', str(a[0][0].strip()), ', ', str(a[0][1].strip()), 'on column land_value_estimate value: ', str(b), '\n')

def update_shr(b, a):
    con = psycopg2.connect(database='owenwilliams', host="localhost", port="5434")
    cur = con.cursor()
    cur.execute("""
        UPDATE county_population_csv cpc
            SET land_share_estimate = %(str)s
                WHERE trim(cpc.state) = %(st)s
                AND trim(cpc.county) = %(cty)s
                AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
                """, {'str':b, 'st':str(a[0][1].strip()), 'cty':str(a[0][0].strip())})
    con.commit()
    print('Database updated, check: ', str(a[0][0].strip()), ', ', str(a[0][1].strip()), 'on column land_share_estimate value: ', str(b), '\n')
    