import requests, json, pandas as pd

# Returns parks (lat, long) from National Park Service API

def parks_get():
    endpoint = "https://developer.nps.gov/api/v1/parks"
    HEADERS = {"X-Api-Key": "Y1YtARnlUdfs8BZ6B74c0jSgQ0M8dZ2uI6cplvsN"}
    params = {"limit":"500"}
    response = requests.get(endpoint, params = params, headers=HEADERS)
    d = response.json()
    parks_data = pd.json_normalize(d['data'])
    return parks_data[["parkCode", "url", "fullName", "latitude", "longitude"]]
