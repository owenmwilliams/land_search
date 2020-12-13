from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct, max
from datetime import datetime

db = "v002"

StartWhile = datetime.now()
print('*********************************', '\n')

spark = SparkSession \
        .builder \
        .appName("dumb_nothingness") \
        .config("spark.jars", "/usr/lib/jvm/java-8-openjdk-arm64/jre/lib/ext/postgresql-42.2.18.jar") \
        .getOrCreate()

pgDF = spark.read.format("jdbc")\
    .option("driver", "org.postgresql.Driver")\
    .option("url", "jdbc:postgresql://pi0:5432/%s" % db)\
    .option("dbtable", "countydataset")\
    .load()

pgDF.select("state").distinct().show()
pgDF.printSchema()

min = pgDF.filter((pgDF.landvalueestimate != 'estimate') & (pgDF.landvalueestimate != 'Not enough comps.')).agg({"landvalueestimate": "min"}).collect()
print(min)

max = pgDF.filter((pgDF.landvalueestimate != 'estimate') & (pgDF.landvalueestimate != 'Not enough comps.')).agg({"landvalueestimate": "max"}).collect()
print(max)

min = pgDF.agg({"landshareestimate": "min"}).collect()
print(min)

max = pgDF.agg({"landshareestimate": "max"}).collect()
print(max)

EndWhile = datetime.now()
print('*********************************', '\n', 'Time for calculation: ', EndWhile - StartWhile)
