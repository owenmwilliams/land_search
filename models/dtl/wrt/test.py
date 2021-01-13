import pyarrow.parquet as pq
import pandas as pd

q = pq.read_table('./file_test/2021-01-12/California')
# t = pd.read_parquet('./file_test/2021-01-12/Delaware.parquet')

t = q.to_pandas()

print(q)
print(t)