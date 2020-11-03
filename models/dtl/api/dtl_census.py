import requests
import json
import pandas as pd

# Returns county population data from Census API - static from 2019; UPDATE to be dynamic search for latest

def census_get():
    response = requests.get('https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=county:*&key=732b0a009f519f9728b9e054d659e8ecf2d9e6fc')
    x = response.json() 
    return pd.read_json(json.dumps(x))
    