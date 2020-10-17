import psycopg2
from datetime import datetime
from psycopg2 import sql
from operator import itemgetter

# timing start
StartTime = datetime.now()

# connecting to the right database
con = psycopg2.connect(database='owenwilliams', host="localhost", port="5434")
Time1 = datetime.now()-StartTime
print("Database opened successfully: ", Time1)

# setting up a cursor
cur = con.cursor()

# get all column names
cur.execute("""BEGIN;
 SELECT lookup_YrCostPopShareAirPark('mycur', 2018::varchar, %(pop)s, %(cost)s, %(share)s::decimal, %(air)s::decimal, %(park_dist)s::decimal, %(park_num)s::integer);
 FETCH ALL IN "mycur";""", {'pop' : 175000, 'cost' : 20000, 'share' : 0.25, 'air' : 1.5, 'park_dist' : 2.5, 'park_num' : 3})
ColumnsArray = cur.fetchall()
print("Array generated: ", datetime.now() - StartTime)
print("Total records: ", len(ColumnsArray), '\n')
#print(ColumnsArray)


# adjust columns array to determine the columns to pull unique values on
states = [x[0] for x in ColumnsArray]
counties = [x[1] for x in ColumnsArray]
for x in range(len(states)):
    print(counties[x], ', ', states[x])

con.close()
