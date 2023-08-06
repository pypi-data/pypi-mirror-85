# Directly plot a line-plot from a pandas DataFrame

attribute = 'MedInc'
data[[attribute]].plot.line(figsize=(8,4), legend=None)
ax = plt.gca()
ax.set_xlabel(attribute, fontsize=14)
ax.set_ylabel('Value', fontsize=14);