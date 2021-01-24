from dtl.api.dtl_census import st_fips_get, census_get
from datetime import date
import os
import json
from pathlib import Path
from pyarrow import parquet as pq
import pyarrow as pa
from dotenv import load_dotenv

# Getting input from API into parquet on HDFS
def to_hdfs(api):
    if api == "Census-demo":
        state_list = st_fips_get()
        today = date.today()
        path = today.strftime("%Y-%m-%d")
        for i in range(len(state_list)):
            record = state_list.iloc[i]
            state = record['state']
            file_name = record['NAME']
            file_name = file_name.rsplit(', ', 1)[1]
            file_name = file_name.replace(" ", "_")
            
            hdfs_save('/ls_raw_dat/census_demo/%s' % path, '%s' % file_name, census_get(state))
    else:
        print('Other APIs links yet to be built.')

def to_local(api):
    if api == "Census-demo":
        state_list = st_fips_get()
        today = date.today()
        path = today.strftime("%Y-%m-%d")
        for i in range(len(state_list)):
            record = state_list.iloc[i]
            state = record['state']
            file_name = record['NAME']
            file_name = file_name.rsplit(', ', 1)[1]
            file_name = file_name.replace(" ", "_")

            outdir = 'Users/owenwilliams/Projects/land_search/file_test/census_demo/%s' % path
            if not os.path.exists(outdir):
                Path(outdir).mkdir(parents=True, exist_ok=True)
            full_path = os.path.join(outdir, file_name)
            
            if not os.path.exists(full_path):
                file_DF = census_get(state)
                
                file_DF.to_parquet(full_path)
                print('File saved: %s' % file_name)
    else:
        print('Other APIs links yet to be built.')

# Save parquet file to HDFS    
def hdfs_save_arrow(path_name, file_name, pDF):
    os.system('hadoop fs -mkdir -p "{0}"'.format(path_name))
    aDF = pa.Table.from_pandas(pDF)
    fs = pa.hdfs.connect(host="pi0", port=54310)
    with fs.open('{0}/{1}'.format(path_name, file_name)) as fw:
        pq.write_table(aDF, fw)

# Workaround - save locally, then put to HDFS    
def hdfs_save(path_name, file_name, pDF):
    load_dotenv()
    ls_home = '{0}/{1}'.format(os.getenv("LSHOME"), path_name)
    if not os.path.exists(ls_home):
        Path(ls_home).mkdir(parents=True, exist_ok=True)

    full_path = os.path.join(ls_home, file_name)
    pDF.to_parquet(full_path)

    os.system('hadoop fs -mkdir -p "{0}"'.format(path_name))
    os.system('hadoop fs -put {0} {1}/{2}'.format(full_path, path_name, file_name))
