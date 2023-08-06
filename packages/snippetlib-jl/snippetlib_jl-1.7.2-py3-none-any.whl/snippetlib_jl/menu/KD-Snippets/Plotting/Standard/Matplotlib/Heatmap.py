# plot a heatmap of a dataframe.
# NOTE, THAT THIS ONLY WORKS ON NUMERIC DATA

fig, ax = plt.subplots(figsize=(10,100))
plot = ax.imshow(data, cmap=plt.cm.RdYlGn, interpolation='nearest')#, vmin=-1, vmax=1)
plt.tick_params(labelbottom='off',labeltop='on')
plt.yticks(range(len(data.index)), np.array(data.index))
plt.xticks(range(len(data.columns)), np.array(data.columns), rotation=90)
plt.colorbar(plot, shrink=0.8)
plt.grid(False)
plt.show()