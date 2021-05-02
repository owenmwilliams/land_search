import requests, json, pandas as pd
import os
from dotenv import load_dotenv

# Get a full list of census county FIPS

# Get the number of records for a given county/year; TODO - add a try except clause & define what to return in case of no data available
def num_records(cty_fips, yr):
    load_dotenv()    
    endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    HEADERS = {"token": os.getenv("NOAA_KEY")}
    start = "{0}-01-01".format(yr)
    end = "{0}-12-31".format(yr)
    location = "FIPS:{0}".format(cty_fips)
    data = "TMAX,TMIN,TAVG,PRCP,SNOW,AWND"
    params = {"limit":"1000", "datasetid":"GHCND", "datatypeid":data, "locationid":location, "startdate":start, "enddate":end}
    response = requests.get(endpoint, params = params, headers=HEADERS)
    d = response.json()
    text = json.dumps(d, sort_keys=True, indent=4)
    numDF = pd.json_normalize(d['metadata'])
    num = int(numDF['resultset.count'])
    return num

# Get tranches of result sets

# Consolidate in one dataframe

# Save as parquet to HDFS

# Returns XXX weather data for counties in a state
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
def weather_get():
    load_dotenv()
    
    endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    HEADERS = {"token": os.getenv("NOAA_KEY")}
    start = "2020-01-01"
    end = "2020-12-31"
    location = "FIPS:25025"
    data = "TMAX,TMIN,TAVG,PRCP,SNOW,AWND"
    params = {"limit":"1000", "datasetid":"GHCND", "datatypeid":data, "locationid":location, "startdate":start, "enddate":end}
    response = requests.get(endpoint, params = params, headers=HEADERS)
    d = response.json()
    pDF = pd.json_normalize(d['results']).drop(columns=['attributes'])#.set_index(['date','station','datatype'])
    print(pDF)
    piv_pDF = pDF.pivot(index=['date', 'station'], columns='datatype', values='value')
    # piv_pDF = pDF.unstack('datatype').reset_index(level='station', col_level=1).reset_index(level='date', col_level=1)
    return piv_pDF



def weather_data_get():
    load_dotenv()
    
    endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/datacategories"
    HEADERS = {"token": os.getenv("NOAA_KEY")}
    params = {"limit":"1000", "datasetid":"GHCND"}
    response = requests.get(endpoint, params = params, headers=HEADERS)
    print(response.text)
    print(response.status_code)
    d = response.json()
    text = json.dumps(d, sort_keys=True, indent=4)
    print(text)

def weather_datacat_get():
    load_dotenv()
    
    endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/datatypes"
    HEADERS = {"token": os.getenv("NOAA_KEY")}
    params = {"limit":"1000", "datasetid":"GHCND"}
    response = requests.get(endpoint, params = params, headers=HEADERS)
    print(response.text)
    print(response.status_code)
    d = response.json()
    text = json.dumps(d, sort_keys=True, indent=4)
    print(text)


def weather_dataloc_get():
    load_dotenv()
    
    endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/locationcategories"
    HEADERS = {"token": os.getenv("NOAA_KEY")}
    params = {"limit":"1000", "datasetid":"GSOM"}
    response = requests.get(endpoint, params = params, headers=HEADERS)
    print(response.text)
    print(response.status_code)
    d = response.json()
    text = json.dumps(d, sort_keys=True, indent=4)
    print(text)