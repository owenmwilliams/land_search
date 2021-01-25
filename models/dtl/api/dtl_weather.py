import requests, json, pandas as pd
import os
from dotenv import load_dotenv

# Returns XXX weather data for counties in a state
pd.set_option('display.max_rows', None)
def weather_get():
    load_dotenv()
    
    endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    HEADERS = {"token": os.getenv("NOAA_KEY")}
    start = "2020-01-01"
    end = "2020-12-31"
    location = "FIPS:36059"
    data = "TMAX,TMIN,TAVG,PRCP,SNOW,AWND"
    params = {"limit":"1000", "datasetid":"GHCND", "datatypeid":data, "locationid":location, "startdate":start, "enddate":end}
    response = requests.get(endpoint, params = params, headers=HEADERS)
    # print(response.text)
    # print(response.status_code)
    d = response.json()
    pDF = pd.json_normalize(d['results']).drop(columns=['attributes']).set_index(['date','station','datatype'])
    print(pDF)
    # columns = pd.Index(['date', 'station'], name = 'item')
    # pDF = pDF.reindex(columns = columns)
    piv_pDF = pDF.unstack('datatype')
    print(piv_pDF)
    # print(pDF.unstack('datatype'))
    # text = json.dumps(d, sort_keys=True, indent=4)
    # print(text)

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