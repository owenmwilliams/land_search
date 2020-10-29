import requests
import json

def census_get():
    response = requests.get('https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=county:*&key=732b0a009f519f9728b9e054d659e8ecf2d9e6fc')
    return response.json()