# Select only the numeric attributes from the dataframe

numeric_attributes = data.columns[[x in [int, float] for x in data.dtypes]]
data = data[numeric_attributes]