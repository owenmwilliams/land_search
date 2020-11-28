from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct, max
from datetime import datetime

StartWhile = datetime.now()
print('*********************************', '\n')

spark = SparkSession \
        .builder \
        .appName("dumb_nothingness") \
        .config("spark.jars", "/Library/Java/Extensions/pgsql_driver.jar") \
        .getOrCreate()

pgDF = spark.read.format("jdbc")\
    .option("driver", "org.postgresql.Driver")\
    .option("url", "jdbc:postgresql://localhost:5437/owenwilliams")\
    .option("dbtable", "full_census")\
    .load()

pgDF.select("name").distinct().show()
pgDF.select(countDistinct("name")).show()
pgDF.select(max("pop")).show()

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)
