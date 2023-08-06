fraction = 1/3
target     = 'Target'
attributes = [c for c in data.columns if c != target]
num_test = int(fraction*len(data))

X_train, X_test = data[attributes].iloc[:-num_test].values, data[attributes].iloc[-num_test:].values
y_train, y_test = data[target].iloc[:-num_test].values,     data[target].iloc[-num_test:].values