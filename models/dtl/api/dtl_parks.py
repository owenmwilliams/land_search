import requests, json, pandas as pd

# Returns parks (lat, long) from National Park Service API

def parks_get():
    endpoint = "https://developer.nps.gov/api/v1/parks"
    HEADERS = {"X-Api-Key": "<INSERT KEY HERE>"}
    params = {"limit":"500"}
    response = requests.get(endpoint, params = params, headers=HEADERS)
    d = response.json()
    parks_data = pd.json_normalize(d['data'])
    return parks_data[["parkCode", "url", "fullName", "latitude", "longitude"]]
