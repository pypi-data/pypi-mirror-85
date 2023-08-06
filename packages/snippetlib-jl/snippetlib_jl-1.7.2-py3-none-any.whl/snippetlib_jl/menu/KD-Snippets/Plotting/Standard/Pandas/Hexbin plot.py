# Directly plot a hexbin-plot from a pandas DataFrame

attribute1 = ''
attribute2 = ''

data.plot.hexbin(x=attribute1, y=attribute2, gridsize=10, cmap='Blues', figsize=(10,6), sharex=False)
ax = plt.gca()
ax.set_xlabel(attribute1, fontsize=14)
ax.set_ylabel(attribute2, fontsize=14);