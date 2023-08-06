# Directly plot a histogram from a pandas DataFrame
attribute = ''

data[[attribute]].plot.hist(bins=15, legend=None, histtype='step', linewidth=2)
ax = plt.gca()
ax.set_xlabel(attribute, fontsize=14)
ax.set_ylabel('Count', fontsize=14);