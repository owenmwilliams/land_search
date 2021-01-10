from dtl.api.dtl_census import st_fips_get, census_get_json
from datetime import date
import os
import json

# Getting input json into HDFS
def to_hdfs(api):
    if api == "Census":
        state_list = st_fips_get()
        date = date.today()
        path = date.strftime("%Y-%m-%d")
        for i in range(len(state_list)):
            record = state_list.iloc[i]
            state = record['state']
            file_name = record['GEONAME']
            file_name.rsplit(', ', 1)[1]
            file_name.replace(" ", "_")
            hdfs_save('/land_search/census/%s' % path, '%s.json' % file_name, census_get_json(state))
    else:
        print('Other APIs links yet to be built.')

def to_local(api):
    if api == "Census":
        state_list = st_fips_get()
        date = date.today()
        path = date.strftime("%Y-%m-%d")
        for i in range(len(state_list)):
            record = state_list.iloc[i]
            state = record['state']
            file_name = record['GEONAME']
            file_name.rsplit(', ', 1)[1]
            file_name.replace(" ", "_")
            local_save('~/Projects/land_search/json/%s' % path, '%s.json' % file_name, census_get_json(state))
    else:
        print('Other APIs links yet to be built.')

# Make directory on HDFS
def hdfs_mkdir(path_name):
    try:
        os.system('hadoop fs -mkdir -p "{0}"'.format(path_name))
    except:
        print('Directory already exists.')

# Make local directory
def local_mkdir(path_name):
    try:
        os.mkdir(path_name)
    except:
        print('Directory already exists.')

# Save JSON file to HDFS    
def hdfs_save(path_name, file_name, file)
    try:
        hdfs_mkdir(path_name)
    finally:
        os.system('echo "{0}" | hadoop fs -put - "{1}/{2}}"'.format(json.dump(file), path_name, file_name))

def local_save(path_name, file_name, file)
    try:
        local_mkdir(path_name)
    finally:
        file = open("{0}/{1}".format(path_name, file_name))
        file.write(json.dump(file))
        file.close()
