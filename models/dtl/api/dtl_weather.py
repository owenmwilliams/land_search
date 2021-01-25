import requests, json, pandas as pd
import os
from dotenv import load_dotenv

# Returns XXX weather data for counties in a state

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
    print(response.text)
    print(response.status_code)
    d = response.json()
    text = json.dumps(d, sort_keys=True, indent=4)
    print(text)

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