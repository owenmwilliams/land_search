import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# Returns county population and demographics data from Census UPDATE to be dynamic search for latest

def census_get(st_fips):
    load_dotenv()
    gets = {"LASTUPDATE,DATE_CODE,NAME,POP,RACE,SEX,AGEGROUP,HISP"}
    fors = {"county:*"}
    ins = {"state:%s" % st_fips}
    params = {"get":gets, "for":fors, "in":ins, "key":os.getenv("CENSUS_KEY")}
    response = requests.get('https://api.census.gov/data/2019/pep/charagegroups', params=params)
    dat = response.json()
    return pd.read_json(json.dumps(dat))
    