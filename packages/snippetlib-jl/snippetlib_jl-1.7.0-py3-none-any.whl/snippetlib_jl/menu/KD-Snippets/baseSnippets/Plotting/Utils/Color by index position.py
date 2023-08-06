# generate a color-gradiend along the indices of a dataframe for a matplotlib plot that 

i = sorted(data.index)
data = data.loc[i]
entries = np.arange(len(data)).astype(float)/len(data)
myColor = plt.cm.hot(entries)