import pyspark
from dtl.scp.scp_loa import scp_loa_cty
from dtl.wrt.wrt_hdfs import hdfs_save


#Define spark context to include python script for returning dataframe
sc = pyspark.SparkContext('local[*]', appName='LOA_SCP', pyFiles='/opt/ls...XXX')


#Get a spark dataframe with each county, state
for k

txt = sc.textFile('/Users/owenwilliams/Projects/land_search/requirements.txt')
print(txt.count())

#Spark dataframe == dataframe from scp_loa_cty
for k in range(len(cty_list)):
    sDF = sc.scp_loa_cty(county, state)


#Save spark dataframe to HDFS with hdfs_save

python_lines = txt.filter(lambda line: 'python' in line.lower())
print(python_lines.count())