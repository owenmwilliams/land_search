import requests, json
from requests.auth import HTTPBasicAuth

def parks_get():
    endpoint = "https://developer.nps.gov/api/v1/parks"
    HEADERS = {"X-Api-Key": "Y1YtARnlUdfs8BZ6B74c0jSgQ0M8dZ2uI6cplvsN"}
#    payload = {"latitude":"*", "longitude":"*", "name":"*"}
    response = requests.get(endpoint, headers=HEADERS)
    return response.json()#["parkCode"]


#payload = {'key1': 'value1', 'key2': 'value2'}
#r = requests.get('https://httpbin.org/get', params=payload)