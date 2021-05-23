from urllib.request import Request, urlopen
import ssl
from bs4 import BeautifulSoup
from datetime import date
import re
from est.db.cur import con_cur
import pandas as pd
import os
from fp.fp import FreeProxy


# #Build url addendum
# cty_list = []
# for i in range(len(cty_array)):
#     if cty_array['State'][i] == 'DE':
#         x = '{0}-{1}'.format(cty_array['County'][i], cty_array['State'][i])
#         x = x.replace(' ', '-')
#         cty_list.append(x)

# #Need to loop through URLs - by county / state, then by page
# for j in range(len(cty_list)):
#     context = ssl._create_unverified_context()
#     url = Request("https://www.landsofamerica.com/{0}/all-land/no-house/".format(cty_list[j]), headers={'User-Agent': 'Mozilla/5.0'})
#     page = urlopen(url, context=context)
#     html = page.read().decode("utf-8")
#     soup = BeautifulSoup(html, "html.parser")

#Return a dataframe with each county and state
def fnd_cty(): 
    cur, con = con_cur()
    cur.execute("""
                    SELECT DISTINCT county, usps FROM countylatlong
                """)
    cty_array = pd.DataFrame(cur.fetchall(), columns = ['County','State'])
    con.close()
    return cty_array

#TODO: add a 'if file exists or was recently downloaded, skip' and IP rotator, set random intervals between requests
def scp_iter():
    cty_array = fnd_cty()
    for i in range(len(cty_array)):
        try:
            pDF = scp_loa_cty(cty_array['County'][i], cty_array['State'][i])
            today = date.today()
            path = '{0}/{1}'.format(today.strftime("%Y-%m-%d"), cty_array['State'][i]).replace(' ', '_')
            file_name = cty_array['County'][i].replace(' ', '_')
            print(path, '...', file_name)
            sv('/ls_raw_dat/lands_of_america/{0}'.format(path), '{0}'.format(file_name), pDF)
        except Exception as e:
            print(e)
            pass

#Takes county name and state abbreviation and returns dataframe with acreage, cost, and location
def scp_loa_cty(county, state):    
    #set up lists
    prc = []
    acr = []
    loc = []
    cty = []
    st = []
    
    #url string
    cty_url = '{0}-{1}'.format(county, state).replace(' ', '-')
    
    #get a proxy
    proxy = FreeProxy(rand=True).get()

    #connect to first page
    context = ssl._create_unverified_context()
    url = Request("https://www.landsofamerica.com/{0}/all-land/no-house/".format(cty_url), headers={'User-Agent': 'Mozilla/5.0'})
    url.set_proxy(proxy, "https")
    page = urlopen(url, context=context)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    #append first page data
    for i in soup.find_all('span', {'class':'_32f8d'}):
        prc.append(i.get_text().strip())
        cty.append(county)
        st.append(state)
    for i in soup.find_all('span', {'class':'_1a278'}):
        acr.append(i.get_text().strip())
    for i in soup.find_all("span"):
        if i.get('title') is not None:
            loc.append(i.get_text().strip())

    #ID # of pages for given county
    page_num = []
    for i in soup.find_all('span', {'class': 'd41b7'}):
        try:
            page_num.append(int(i.get_text().strip()))
        except:
            pass

    #Iterate through all pages in county
    k=2
    while k <= max(page_num):
        context = ssl._create_unverified_context()
        url = Request("https://www.landsofamerica.com/{0}/all-land/no-house/page-{1}".format(cty_url, k), headers={'User-Agent': 'Mozilla/5.0'})
        url.set_proxy(proxy, "https")
        page = urlopen(url, context=context)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        for i in soup.find_all('span', {'class':'_32f8d'}):
            prc.append(i.get_text().strip())
            cty.append(county)
            st.append(state)
        for i in soup.find_all('span', {'class':'_1a278'}):
            acr.append(i.get_text().strip())
        for i in soup.find_all("span"):
            if i.get('title') is not None:
                loc.append(i.get('title'))

        k=k+1

    df = pd.DataFrame(list(zip(prc, acr, loc, cty, st)), columns = ['Price', 'Acreage', 'Location', 'County', 'State'])
    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)
    pd.set_option ("max_colwidth", 30)
    return df