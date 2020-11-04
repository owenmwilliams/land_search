import requests, json

# Returns airports (lat, long, departures, connections) from ICAO API

#### THIS WILL NOT WORK LONG TERM BECAUSE ICAO LIMITS TO 100 CALLS AND MORE CALLS IS MORE $$$

def airports_get():
    endpoint = "https://applications.icao.int/dataservices/api/indicators-list"
    params = dict(api_key="<INSERT KEY HERE>", state="USA", airports="", format="json")
    response = requests.get(endpoint, params = params)
    airports_data = response.json()
    return airports_data

def departures_get():
    endpoint = "https://applications.icao.int/dataservices/api/airport-departure-stats"
    params = dict(api_key="<INSERT KEY HERE>", states="USA", airports="", format="json", year="2019")
    response = requests.get(endpoint, params = params)
    departure_data = response.json()
    return departure_data
