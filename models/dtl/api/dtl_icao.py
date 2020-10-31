import requests, json, pandas as pd

# Returns airports (lat, long, departures, connections) from ICAO API

#### THIS WILL NOT WORK LONG TERM BECAUSE ICAO LIMITS TO 100 CALLS AND MORE CALLS IS MORE $$$

def airports_get():
    endpoint = "https://applications.icao.int/dataservices/api/indicators-list"
    params = dict(api_key="c4e75ea0-1bb5-11eb-a797-cf67e1390e1e", state="USA", airports="", format="json")
    response = requests.get(endpoint, params = params)
    d = response.json()
    airports_data = pd.read_json(json.dumps(d))
    airports_data.to_csv('icao_data', index_label='id', sep=',')
