
import pandas as pd

# Read in data in csv format
# Commented are some typical first preprocessing operations

filename = ""
data = pd.read_csv(filename, delimiter=',', encoding='utf-8')

# Drop rows with NaN values and re-index
#data = data.dropna(axis=0)
#data.index = range(len(data))

# Fill nan values with zeros
#data = data.fillna(0.0)

# Drop attribute 'Id' from data frame
#data = data.drop('Id', axis=1)

# Set attribute 'time' as index
#data = data.set_index('time')

data.head()