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


df = pd.DataFrame(columns = ['Price', 'Acreage', 'Location', 'County'])
#Need to loop through URLs - by county / state, then by page
for j in range(len(cty_list)):
    context = ssl._create_unverified_context()
    url = Request("https://www.landsofamerica.com/{0}/all-land/no-house/".format(cty_list[j]), headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(url, context=context)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    for i in soup.find_all('span', {'class':'_32f8d'}):
        df.at[i, 'Price'] = i.get_text().strip()

    for i in soup.find_all('span', {'class':'_1a278'}):
        df.at[i, 'Acreage'] = i.get_text().strip()

    for i in soup.find_all("span"):
        if i.get('title') is not None:
            df.at[i, 'Location'] = i.get_text().strip()

    #Need to id # of pages for given county
    page_num = []
    for i in soup.find_all('span', {'class': 'd41b7'}):
        try:
            page_num.append(int(i.get_text().strip()))
        except:
            pass

    print(page_num)

    k=2
    while k <= max(page_num):
        context = ssl._create_unverified_context()
        url = Request("https://www.landsofamerica.com/{0}/all-land/no-house/page-{1}".format(cty_list[j], k), headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(url, context=context)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        #Need to build into array / pDF, set data type, and save to parquet files
        for i in soup.find_all('span', {'class':'_32f8d'}):
            print(i.get_text().strip())


        for i in soup.find_all('span', {'class':'_1a278'}):
            print(i.get_text().strip())

        for i in soup.find_all("span"):
            if i.get('title') is not None:
                print(i.get('title'))

        k=k+1


print(df)