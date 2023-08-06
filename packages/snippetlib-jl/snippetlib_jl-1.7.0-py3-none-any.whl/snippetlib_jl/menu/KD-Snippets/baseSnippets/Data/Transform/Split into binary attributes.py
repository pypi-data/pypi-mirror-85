# List of categorical attributes that shall be split into index attributes

to_split = data.columns[data.dtypes == object].tolist()

# Append the former categorical attributes as index attributes
for s in to_split:
    split = pd.get_dummies(data[s])
    column_names = ["%s(=%s)"%(s,x) for x in split.columns]
    split.columns = column_names
    data[column_names] = split

# Delete the original categorical attribute
for s in to_split:
    data.drop(s, axis=1, inplace=True)