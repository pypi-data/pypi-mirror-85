# Directly plot a scatter-plot from a pandas DataFrame

attribute1 = ''
attribute2 = ''

data.plot.scatter(x=attribute1, y=attribute2, figsize=(10,6), alpha=0.5, s=50)
ax = plt.gca()
ax.set_xlabel(attribute1, fontsize=14)
ax.set_ylabel(attribute2, fontsize=14);