import pyspark

sc = pyspark.SparkContext('local[*]')

txt = sc.textFile('/Users/owenwilliams/Projects/land_search/requirements.txt')
print(txt.count())

python_lines = txt.filter(lambda line: 'python' in line.lower())
print(python_lines.count())