import requests
import json
import pandas as pd

# Returns geometry rings for counties from ArcGIS API; returns 2000 rows - UPDATE to return all counties, calc (lat, long) Centroids

def shp_get():
    response = requests.get('https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Counties_Generalized/FeatureServer/0/query?where=1%3D1&outFields=NAME,STATE_NAME,STATE_FIPS,CNTY_FIPS,HSE_UNITS,SQMI,OBJECTID&outSR=4326&f=json')
    d = response.json()
    loc_data = pd.json_normalize(d['features'])
    return loc_data