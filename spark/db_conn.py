from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct, max
from datetime import datetime

StartWhile = datetime.now()
print('*********************************', '\n')

spark = SparkSession \
        .builder \
        .appName("dumb_nothingness") \
        .config("spark.jars", "/usr/lib/jvm/java-8-openjdk-arm64/jre/lib/ext/postgresql-42.2.18.jar") \
        .getOrCreate()

pgDF = spark.read.format("jdbc")\
    .option("driver", "org.postgresql.Driver")\
    .option("url", "jdbc:postgresql://pi0:5434/owenwilliams")\
    .option("dbtable", "county_population_csv")\
    .load()

pgDF.select("state").distinct().show()
pgDF.select(min("land_value_estimate")).show()

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)
