from urllib.request import Request, urlopen
import ssl
from bs4 import BeautifulSoup
import re
from est.db.cur import con_cur
import pandas as pd

#Need full set of counties & states
cur, con = con_cur()
cur.execute("""
                SELECT DISTINCT county, usps FROM countylatlong
            """)
cty_array = pd.DataFrame(cur.fetchall(), columns = ['County','State'])
con.close()

#Build url addendum
cty_list = []
for i in range(len(cty_array)):
    if cty_array['State'][i] == 'CA':
        x = '{0}-{1}'.format(cty_array['County'][i], cty_array['State'][i])
        x = x.replace(' ', '-')
        cty_list.append(x)
print(cty_list)

#Need to loop through URLs - by county / state, then by page
context = ssl._create_unverified_context()
url = Request("https://www.landsofamerica.com/Yolo-County-CA/all-land/no-house/", headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(url, context=context)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

#Need to id # of pages for given county
page_num = []
for i in soup.find_all('span', {'class': 'd41b7'}):
    try:
        page_num.append(int(i.get_text().strip()))
    except:
        pass
print(max(page_num))

#Need to build into array / pDF, set data type, and save to parquet files
for i in soup.find_all('span', {'class':'_32f8d'}):
    print(i.get_text().strip())

for i in soup.find_all('span', {'class':'_1a278'}):
    print(i.get_text().strip())

for i in soup.find_all("span"):
    if i.get('title') is not None:
        print(i.get('title'))