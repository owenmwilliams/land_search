import requests
import json
import pandas as pd

# Returns county population and demographics data from Census UPDATE to be dynamic search for latest

def census_get():
    gets = {"LASTUPDATE,DATE_CODE,NAME,POP,RACE,SEX,AGEGROUP,HISP"}
    fors = {"county:*"}
    ins = {"STATE:01"}
    params = {"get":gets, "for":fors, "in":ins, "key":"<INSERT KEY HERE>"}
    response = requests.get('https://api.census.gov/data/2019/pep/charagegroups', params=params)
    dat = response.json()
    return pd.read_json(json.dumps(dat))