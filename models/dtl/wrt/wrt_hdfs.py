import dtl.api.dtl_census as cs
import dtl.api.dtl_parks as np
from datetime import date
import os
import json
from pathlib import Path
from pyarrow import parquet as pq
import pyarrow as pa
from dotenv import load_dotenv

# Getting input from API into parquet on HDFS
def to_hdfs(api):
    state_list = cs.st_fips_get()
    today = date.today()
    path = today.strftime("%Y-%m-%d")
    for i in range(len(state_list)):
        record = state_list.iloc[i]
        state = record['state']
        file_name = record['NAME']
        file_name = file_name.rsplit(', ', 1)[1]
        file_name = file_name.replace(" ", "_")
        if api == "Census-demo":
            hdfs_save('/ls_raw_dat/census_demo/%s' % path, '%s' % file_name, cs.census_get(state))
        elif api == "Census-time":
            hdfs_save('/ls_raw_dat/census_time/%s' % path, '%s' % file_name, cs.census_time_get(state))
        elif api == "Census-house":
            try:
                hdfs_save('/ls_raw_dat/census_housing/%s' % path, '%s' % file_name, cs.census_housing_get(state))
            except:
                print('*****')
                print('Could not download state: %s' % file_name)
                print('#####')                
        elif api == "National-parks":
            file_name = "National_parks"
            hdfs_save('/ls_raw_dat/national_parks/%s' % path, '%s' % file_name, np.parks_get())
            break
        else:
            print('Other APIs links yet to be built.')

def to_local(api):
    if api == "Census-demo":
        state_list = cs.st_fips_get()
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
                file_DF = cs.census_get(state)
                
                file_DF.to_parquet(full_path)
                print('File saved: %s' % file_name)
    else:
        print('Other APIs links yet to be built.')

# Save parquet file to HDFS    
def hdfs_save_arrow(path_name, file_name, pDF):
    os.system('hadoop fs -mkdir -p "{0}"'.format(path_name))
    print(pDF)
    aDF = pa.Table.from_pandas(pDF)
    print('{0}/{1}'.format(path_name, file_name))
    hdfs = fs.HadoopFileSystem(host="pi0", port=54310, user=hduser)
    with hdfs.open_output_stream('{0}/{1}.parquet'.format(path_name, file_name), "wb") as fw:
        pq.write_table(aDF, fw)      
    # pq.write_to_dataset(aDF, '{0}/{1}'.format(path_name, file_name), filesystem=hdfs)
    pq.write_table(aDF, '{0}/{1}'.format(path_name, file_name), filesystem=hdfs)

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
