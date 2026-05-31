import pyarrow.parquet as pq

archivo = 'datos_hive/yellow_tripdata_2026-01.parquet'
esquema = pq.read_schema(archivo)

print("-" * 50)
print(esquema)
