import dtl.wrt.wrt_hdfs as sv
from bs4 import BeautifulSoup
from datetime import date
from est.db.cur import con_cur
import pandas as pd
import requests
import proxyscrape

#TODO: add a 'if file exists or was recently downloaded, skip' and IP rotator, set random intervals between requests
def scp_iter():
    collector = proxyscrape.create_collector('my-collector', 'https')
    cty_array = fnd_cty()
    for i in range(len(cty_array)):
        try:
            pDF = scp_loa_cty(cty_array['County'][i], cty_array['State'][i])
            print(pDF)
            today = date.today()
            path = '{0}/{1}'.format(today.strftime("%Y-%m-%d"), cty_array['State'][i]).replace(' ', '_')
            file_name = cty_array['County'][i].replace(' ', '_')
            print(path, '...', file_name)
            sv.wrt_hdfs('/ls_raw_dat/lands_of_america/{0}'.format(path), '{0}'.format(file_name), pDF)
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
    cty_url_1 = build_url(county, state, 1)
    pg1_text, proxy = proxy_iterate(cty_url_1)
    total_pages = find_page_num(pg1_text)
    prc1, acr1, loc1, cty1, st1 = pg_parse(pg1_text, county, state)

    prc.extend(prc1)
    acr.extend(acr1)
    loc.extend(loc1)
    cty.extend(cty1)
    st.extend(st1)
    
    for i in range(total_pages - 1):
        cty_url = build_url(county, state, i+1)
        pg_text = get_page_text(cty_url, proxy)
        prcn, acrn, locn, ctyn, stn = pg_parse(pg_text, county, state)
        prc.extend(prcn)
        acr.extend(acrn)
        loc.extend(locn)
        cty.extend(ctyn)
        st.extend(stn)

    df = pd.DataFrame(list(zip(prc, acr, loc, cty, st)), columns = ['Price', 'Acreage', 'Location', 'County', 'State'])
    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)
    pd.set_option ("max_colwidth", 30)
    return df

def pg_parse(html, county, state):
    prc = []
    acr = []
    loc = []
    cty = []
    st = []
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
    return prc, acr, loc, cty, st

def get_https_proxy(collector):   
    proxy = collector.get_proxy({'type':'https'})
    proxies = {'https': 'https://{0}:{1}'.format(proxy[0],proxy[1])}
    return proxies

def get_page_text(url, proxies):
    headers={'User-Agent': 'Mozilla/5.0'}
    html = requests.get(url, verify=False, headers=headers, proxies=proxies, timeout=2.0)
    return html.text

def proxy_iterate(url):
    while True:
        collector = proxyscrape.get_collector('my-collector')
        proxy = get_https_proxy(collector)
        print(proxy)
        try:
            html = get_page_text(url, proxy)
            return html, proxy
            break
        except:
            continue

def find_page_num(html):
    page_num = []
    soup = BeautifulSoup(html, "html.parser")
    for i in soup.find_all('span', {'class': 'd41b7'}):
        try:
            page_num.append(int(i.get_text().strip()))
        except:
            pass
    return max(page_num)

def build_url(county, state, page):
    cty_url = '{0}-{1}'.format(county, state).replace(' ', '-')
    url = "https://www.landsofamerica.com/{0}/all-land/no-house/page-{1}".format(cty_url, page)
    return url

#Return a dataframe with each county and state
def fnd_cty(): 
    cur, con = con_cur()
    cur.execute("""
                    SELECT DISTINCT county, usps FROM countylatlong
                """)
    cty_array = pd.DataFrame(cur.fetchall(), columns = ['County','State'])
    con.close()
    return cty_array