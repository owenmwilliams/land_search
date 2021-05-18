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
    if cty_array['State'][i] == 'DE':
        x = '{0}-{1}'.format(cty_array['County'][i], cty_array['State'][i])
        x = x.replace(' ', '-')
        cty_list.append(x)
print(cty_list)



prc = []
acr = []
loc = []

#Need to loop through URLs - by county / state, then by page
for j in range(len(cty_list)):
    context = ssl._create_unverified_context()
    url = Request("https://www.landsofamerica.com/{0}/all-land/no-house/".format(cty_list[j]), headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(url, context=context)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    for i in soup.find_all('span', {'class':'_32f8d'}):
        prc.append(i.get_text().strip())

    for i in soup.find_all('span', {'class':'_1a278'}):
        acr.append(i.get_text().strip())

    for i in soup.find_all("span"):
        if i.get('title') is not None:
            loc.append(i.get_text().strip())

    #Need to id # of pages for given county
    page_num = []
    for i in soup.find_all('span', {'class': 'd41b7'}):
        try:
            page_num.append(int(i.get_text().strip()))
        except:
            pass

    k=2
    while k <= max(page_num):
        context = ssl._create_unverified_context()
        url = Request("https://www.landsofamerica.com/{0}/all-land/no-house/page-{1}".format(cty_list[j], k), headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(url, context=context)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        #Need to build into array / pDF, set data type, and save to parquet files
        for i in soup.find_all('span', {'class':'_32f8d'}):
            prc.append(i.get_text().strip())

        for i in soup.find_all('span', {'class':'_1a278'}):
            acr.append(i.get_text().strip())

        for i in soup.find_all("span"):
            if i.get('title') is not None:
                loc.append(i.get('title'))

        k=k+1

df = pd.DataFrame(list(zip(prc, acr, loc)), columns = ['Price', 'Acreage', 'Location'])
pd.set_option("max_rows", None)
pd.set_option("max_columns", None)
print(df)