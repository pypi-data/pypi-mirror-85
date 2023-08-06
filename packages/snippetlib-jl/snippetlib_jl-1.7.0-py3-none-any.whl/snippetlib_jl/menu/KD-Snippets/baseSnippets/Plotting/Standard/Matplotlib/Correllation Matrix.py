# plot a colored correllation matrix.
# NOTE, THAT THIS ONLY WORKS ON NUMERIC DATA

corr = data.corr()

import scipy.cluster.hierarchy as hierarchy
Y = hierarchy.linkage(corr)
sorting = hierarchy.leaves_list(Y)
corr = corr.values[sorting].T[sorting]

fig, ax = plt.subplots(figsize=(8,8))
plot = ax.imshow(corr, cmap=plt.cm.RdYlGn, interpolation='nearest', vmin=-1, vmax=1)
plt.tick_params(labelbottom='off',labeltop='on')
plt.xticks(range(len(data.columns)), np.array(data.columns)[sorting], rotation=90)
plt.yticks(range(len(data.columns)), np.array(data.columns)[sorting])
plt.colorbar(plot, shrink=0.8)
plt.grid(False)
plt.show()