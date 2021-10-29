#%%
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "stock"
org = "whu"
token = "P50-P5exJPdxfqX1hSlZuAt1Qfqa-VDdeUaboL9Ec2mSJb8rWnkjt3SP9jYyblFcA4pEQ732FMFAdEW8TT4YUA=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org,
)

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
write_api.write(bucket=bucket, org=org, record=p)

#%%
import pandas as pd 
query_api = client.query_api()
query = '''
from(bucket:"stock")
|> range(start:-10m)
|> filter(fn:(r)=>r._measurement == "my_measurement")
|> filter(fn: (r) => r.location == "Prague")
|>filter(fn:(r) => r._field == "temperature")
'''
result = query_api.query_data_frame(org=org, query=query)

