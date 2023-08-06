# Normalize the data

from sklearn.preprocessing import StandardScaler, MinMaxScaler

# subtract mean & divide by std
#scaler = StandardScaler()

# scale data between 0 & 1
scaler = MinMaxScaler(feature_range=(0, 1))

scaler.fit(data)
sdata = scaler.transform(data)

# un-scale the data back into their original value domain
#scaler.inverse_transform()
