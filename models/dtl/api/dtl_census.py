import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

# Returns county population and demographics data from Census 
# TODO: condense census get functions to return pDF or JSON

def census_get(st_fips):
    load_dotenv()
    gets = {"LASTUPDATE,NAME,POP,RACE,SEX,AGEGROUP,HISP"}
    fors = {"county:*"}
    ins = {"state:%s" % st_fips}
    params = {"get":gets, "for":fors, "in":ins, "key":os.getenv("CENSUS_KEY")}
    response = requests.get('https://api.census.gov/data/2019/pep/charagegroups', params=params)
    dat = response.json()
    pDF = pd.read_json(json.dumps(dat))
    new_header = pDF.iloc[0]
    pDF = pDF[1:]
    pDF.columns = new_header
    return pDF

def census_time_get(st_fips):
    load_dotenv()
    gets = {"LASTUPDATE,NAME,POP,DATE_CODE,AGEGROUP"}
    fors = {"county:*"}
    ins = {"state:%s" % st_fips}
    params = {"get":gets, "for":fors, "in":ins, "key":os.getenv("CENSUS_KEY")}
    response = requests.get('https://api.census.gov/data/2019/pep/charagegroups', params=params)
    dat = response.json()
    pDF = pd.read_json(json.dumps(dat))
    new_header = pDF.iloc[0]
    pDF = pDF[1:]
    pDF.columns = new_header
    return pDF

def census_housing_get(st_fips):  
    load_dotenv()
    gets = {"LASTUPDATE,NAME,DATE_CODE,DATE_DESC,HUEST"}
    fors = {"county:*"}
    ins = {"state:%s" % st_fips}
    params = {"get":gets, "for":fors, "in":ins, "key":os.getenv("CENSUS_KEY")}
    response = requests.get('https://api.census.gov/data/2019/pep/housing', params=params)
    dat = response.json()
    pDF = pd.read_json(json.dumps(dat))
    new_header = pDF.iloc[0]
    pDF = pDF[1:]
    pDF.columns = new_header
    return pDF

def st_fips_get():
    load_dotenv()
    gets = {"NAME"}
    fors = {"county:*"}
    ins = {"state:*"}
    params = {"get":gets, "for":fors, "in":ins, "key":os.getenv("CENSUS_KEY")}
    response = requests.get('https://api.census.gov/data/2019/pep/charagegroups', params=params)
    dat = response.json()
    pDF = pd.read_json(json.dumps(dat))
    new_header = pDF.iloc[0]
    pDF = pDF[1:]
    pDF.columns = new_header
    pDF.drop_duplicates(subset=['state'], inplace=True)
    return pDF
