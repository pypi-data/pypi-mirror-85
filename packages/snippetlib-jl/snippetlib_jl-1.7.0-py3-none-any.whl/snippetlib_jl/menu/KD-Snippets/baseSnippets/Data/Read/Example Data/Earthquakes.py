# Load earthquake data of the last 30 days
import pandas as pd
filename = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"
data = pd.read_csv(filename)

# filter only original Richter-Scale measured earthquakes
data = data[data.magType == 'ml'] 
data = data[['time', 'latitude', 'longitude', 'depth', 'mag', 'dmin']]

# drop nan's
data = data.dropna(axis=0)

# Set timestamp as index
# 2016-01-05T08:38:21.150Z
format = '%Y-%m-%dT%H:%M:%S.%fZ'
data['time'] = pd.to_datetime(data['time'], format=format)
data = data.set_index(['time'])

print(len(data), "earthquakes")
data.head()