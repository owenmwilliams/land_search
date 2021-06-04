import dtl.wrt.wrt_hdfs as sv
from bs4 import BeautifulSoup
from datetime import date
from est.db.cur import con_cur
import pandas as pd
import requests
import proxyscrape
import subprocess
import re

#TODO: add a 'if file exists or was recently downloaded, skip' and IP rotator, set random intervals between requests
def scp_iter():
    collector = proxyscrape.create_collector('my-collector', 'https')
    cty_array = fnd_cty()
    exist_cty_array = existing_cty()
    ret_cty = pd.merge(cty_array, exist_cty_array, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
    ret_cty.drop_duplicates(inplace=True)
#    cty_array = cty_array.sample(frac=1).reset_index(drop=True)
    for i in range(len(ret_cty)):
        try:
            pDF = scp_loa_cty(ret_cty['County'][i], ret_cty['State'][i])
            print(pDF)
            today = date.today()
            path = '{0}/{1}'.format(today.strftime("%Y-%m-%d"), ret_cty['State'][i]).replace(' ', '_')
            file_name = ret_cty['County'][i].replace(' ', '_')
            print(path, '...', file_name)
            sv.hdfs_save('/ls_raw_dat/lands_of_america/{0}'.format(path), '{0}'.format(file_name), pDF)
        except ConnectionAbortedError as err:
            print('Handling error:', err, '. Skipping to next county.')
            pass
        except Exception as e:
            print(e)
            pass

#Takes county name and state abbreviation and returns dataframe with acreage, cost, and location
def scp_loa_cty(county, state):
    print('Getting:{0}, {1}'.format(county, state))
    try:
        collector = proxyscrape.create_collector('my-collector', 'https')
    except:
        collector = proxyscrape.get_collector('my-collector')
    
    #set up lists
    prc = []
    acr = []
    loc = []
    cty = []
    st = []
    
    #url string
    cty_url_1 = build_url(county, state, 1)
    try:
        pg1_text, proxy = proxy_iterate(cty_url_1)
    except ConnectionAbortedError as err:
        return err      
    total_pages = find_page_num(pg1_text)
    prc1, acr1, loc1, cty1, st1 = pg_parse(pg1_text, county, state)

    prc.extend(prc1)
    acr.extend(acr1)
    loc.extend(loc1)
    cty.extend(cty1)
    st.extend(st1)
    
    for i in range(total_pages - 1):
        cty_url = build_url(county, state, i+2)
        try:
            pg_text = get_page_text(cty_url, proxy)
        except ConnectionAbortedError as err:
            return err
        except:
            pg_text, proxy = proxy_iterate(cty_url)
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
    for div in soup.find_all('div', {'class':'_4d28e c2799'}):
        for span in div.find_all('span', {'class':'_32f8d'}):
            prc.append(span.get_text().strip())
            cty.append(county)
            st.append(state)
        for span in div.find_all('span', {'class':'_1a278'}):
            acr.append(span.get_text().strip())
        for span in div.find_all("span"):
            if span.get('title') is not None:
                loc.append(span.get('title'))
    return prc, acr, loc, cty, st

def get_https_proxy(collector):   
    proxy = collector.get_proxy({'type':'https'})
    proxies = {'https': 'https://{0}:{1}'.format(proxy[0],proxy[1])}
    return proxies

#TODO - need to add a catch if the county cannot be found (http 404), or else continuously tries through proxy
def get_page_text(url, proxies):
    headers={'User-Agent': 'Mozilla/5.0'}
    html = requests.get(url, verify=False, headers=headers, proxies=proxies, timeout=10.0)
    if html.status_code == 404:
        return ConnectionAbortedError('Page not found.')
    else:
        if html.status_code == 200:
            expected_length = html.headers.get('Content-Length')
            if expected_length is not None:
                actual_length = html.raw.tell()
                expected_length = int(expected_length)
                if actual_length == expected_length:
                    return html.text
                else:
                    raise IOError('incomplete read')
        else:
            raise IOError('access denied')

def proxy_iterate(url):
    while True:
        collector = proxyscrape.get_collector('my-collector')
        proxy = get_https_proxy(collector)
        print(proxy)
        try:
            html = get_page_text(url, proxy)
            return html, proxy
        except ConnectionAbortedError as err:
            return err        
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
    if len(page_num) > 1:
        return max(page_num)
    else:
        return 1

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

#TODO - only return counties if retrieved recently
def existing_cty():
    counties = pd.DataFrame(columns = ['Core_dir', 'Web_dir', 'Date', 'State', 'County'])
    p = subprocess.Popen("hdfs dfs -ls -R /ls_raw_dat/lands_of_america",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    for line in p.stdout:
        raw_line = line.rstrip()
        text = re.findall(r"\bls_raw\S+County\b", raw_line.decode('utf-8'))
        if text:
            row = text[0].split('/')
            length = len(counties)
            counties.loc[length] = row
    counties.drop(columns=['Core_dir', 'Web_dir', 'Date'], inplace=True)
    counties['County'] = counties['County'].str.replace('_', ' ')
    return counties