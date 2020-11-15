import pyspark
from pyspark.sql import SparkSession

spark = SparkSession \
        .builder \
        .appName("dumb_nothingness") \
        .config("spark.jars", "/Library/Java/Extensions/pgsql_driver.jar") \
        .getOrCreate()

pgDF = spark.read.format("jdbc")\
    .option("driver", "org.postgresql.Driver")\
    .option("url", "jdbc:postgresql://localhost:5434/owenwilliams")\
    .option("dbtable", "public.county_landdata_csv")\
    .load()

pgDF.select("county").distinct().show()